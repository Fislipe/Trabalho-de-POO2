from flask import Flask, render_template, request, redirect, url_for, session
from Classes.facade import SistemaImobiliarioFacade

app = Flask(__name__)
app.secret_key = '7b91e4f2c8a0d3b6f5e8a1c4b9d7e0f2'

#listas locais para testar antes de ligar a base de dados definitiva
usuarios_banco_local = {}
chamados_banco_local = {}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        perfil = request.form.get('perfil')
        nome = request.form.get('nome')
        documento = request.form.get('documento')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        try:
            #chama a fachada para criar o tipo de utilizador correto usando a Factory
            novo_usuario = SistemaImobiliarioFacade.registrar_novo_usuario(perfil, nome, documento, email, senha)
            usuarios_banco_local[email] = novo_usuario
            return redirect(url_for('login'))
        except ValueError as e:
            return f"Erro ao registar: {str(e)}"
            
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = usuarios_banco_local.get(email)
        if usuario and usuario.validar_senha(senha):
            session['usuario_email'] = email
            session['usuario_perfil'] = usuario.obter_perfil()
            
            #encaminha para a tela certa baseado no perfil devolvido
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
            return "Dados incorretos ou não encontrados."
            
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
        
        # Cria o chamado centralizado pela fachada
        novo_chamado = SistemaImobiliarioFacade.abrir_novo_chamado(titulo, descricao, categoria)
        chamados_banco_local[novo_chamado.id] = novo_chamado
        return redirect(url_for('lista_chamados'))
        
    return render_template('abrir_chamado.html')

@app.route('/chamados')
def lista_chamados():
    return render_template('lista_chamados.html', chamados=chamados_banco_local.values())

@app.route('/atualizar_chamado/<chamado_id>')
def atualizar_chamado(chamado_id):
    chamado = chamados_banco_local.get(chamado_id)
    if chamado:
#avança o status do chamado seguindo o state
        SistemaImobiliarioFacade.atualizar_andamento_chamado(chamado)
    return redirect(url_for('lista_chamados'))

if __name__ == '__main__':
    app.run(debug=True)