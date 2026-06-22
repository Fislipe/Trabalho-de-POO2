from flask import Flask, render_template, request, redirect, url_for, session
from Classes.facade import SistemaImobiliarioFacade

app = Flask(__name__)
app.secret_key = '7b91e4f2c8a0d3b6f5e8a1c4b9d7e0f2'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        perfil = request.form.get('perfil')
        nome = request.form.get('nome')
        documento = request.form.get('novo_usuario') 
        email = request.form.get('novo_usuario')
        senha = request.form.get('senha')
        
        try:
            SistemaImobiliarioFacade.registrar_novo_usuario(perfil, nome, documento, email, senha)
            return redirect(url_for('login'))
        except Exception as e:
            return f"Erro ao registar: {str(e)}"
            
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('usuario')
        senha = request.form.get('senha')
        
        usuario = SistemaImobiliarioFacade.autenticar_usuario(email, senha)
        
        if usuario:
            session['usuario_email'] = email
            session['usuario_perfil'] = usuario.obter_perfil()
            
            perfil_nome = usuario.obter_perfil().lower()
            if 'inquilino' in perfil_nome:
                return redirect(url_for('painel_inquilino'))
            elif 'proprietario' in perfil_nome or 'proprietário' in perfil_nome:
                return redirect(url_for('painel_proprietario'))
            elif 'imobiliaria' in perfil_nome or 'imobiliária' in perfil_nome:
                return redirect(url_for('painel_imobiliaria'))
            elif 'prestador' in perfil_nome or 'serviço' in perfil_nome or 'servico' in perfil_nome:
                return redirect(url_for('painel_prestador'))
        else:
            return render_template('login.html', erro="Dados incorretos ou não encontrados.")
            
    return render_template('login.html')

@app.route('/painel_inquilino')
def painel_inquilino():
    return render_template('painel_inquilino.html')

@app.route('/painel_proprietario')
def painel_proprietario():
    return render_template('painel_proprietario.html')

@app.route('/painel_imobiliaria')
def painel_imobiliaria():
    return render_template('painel_imobiliaria.html')

@app.route('/painel_prestador')
def painel_prestador():
    return render_template('painel_prestador.html')

@app.route('/abrir_chamado', methods=['GET', 'POST'])
def abrir_chamado():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        criado_por = session.get('usuario_email')
        
        SistemaImobiliarioFacade.abrir_novo_chamado(titulo, descricao, categoria, criado_por)
        return redirect(url_for('meus_chamados'))
        
    return render_template('abrir_chamado.html')

@app.route('/chamados')
def lista_chamados():
    chamados_agencia = SistemaImobiliarioFacade.buscar_chamados_imobiliaria()
    return render_template('lista_chamados.html', chamados=chamados_agencia)

@app.route('/escolher_prestador/<chamado_id>', methods=['GET', 'POST'])
def escolher_prestador(chamado_id):
    if request.method == 'POST':
        prestador_email = request.form.get('prestador_email')
        chamado = SistemaImobiliarioFacade.buscar_chamado_por_id(chamado_id)
        
        if chamado and prestador_email:
            # Executa a atribuição salvando o prestador e avançando o State do chamado
            SistemaImobiliarioFacade.atribuir_chamado_a_prestador(chamado, prestador_email)
            
        return redirect(url_for('lista_chamados'))
        
    chamado = SistemaImobiliarioFacade.buscar_chamado_por_id(chamado_id)
    prestadores = SistemaImobiliarioFacade.buscar_todos_prestadores()
    return render_template('escolher_prestador.html', chamado=chamado, prestadores=prestadores)

@app.route('/avancar_chamado/<chamado_id>')
def avancar_chamado(chamado_id):
    chamado = SistemaImobiliarioFacade.buscar_chamado_por_id(chamado_id)
    if chamado:
        SistemaImobiliarioFacade.atualizar_andamento_chamado(chamado)
    
    perfil = session.get('usuario_perfil', '').lower()
    if 'proprietario' in perfil or 'proprietário' in perfil:
        return redirect(url_for('chamados_estruturais'))
    else:
        return redirect(url_for('meus_servicos'))

@app.route('/confirmar_reparo/<chamado_id>')
def confirmar_reparo(chamado_id):
    chamado = SistemaImobiliarioFacade.buscar_chamado_por_id(chamado_id)
    if chamado:
        SistemaImobiliarioFacade.inquilino_confirmar_reparo(chamado)
        SistemaImobiliarioFacade.atualizar_andamento_chamado(chamado)
    return redirect(url_for('meus_chamados'))

@app.route('/meus_chamados')
def meus_chamados():
    email = session.get('usuario_email')
    chamados_do_usuario = SistemaImobiliarioFacade.buscar_chamados_por_usuario(email)
    return render_template('meus_chamados.html', chamados=chamados_do_usuario)

@app.route('/chamados_estruturais')
def chamados_estruturais():
    chamados_pendentes = SistemaImobiliarioFacade.buscar_chamados_estruturais()
    return render_template('chamados_estruturais.html', chamados=chamados_pendentes)

@app.route('/meus_servicos')
def meus_servicos():
    # Pega o e-mail do prestador logado para listar apenas as ordens de serviço DELE
    email = session.get('usuario_email')
    servicos_atribuidos = SistemaImobiliarioFacade.buscar_chamados_prestador(email)
    return render_template('meus_servicos.html', chamados=servicos_atribuidos)

if __name__ == '__main__':
    app.run(debug=True)