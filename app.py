from flask import Flask, render_template, request

app = Flask(__name__)

banco_usuarios = {
    "imobiliaria": "Imobiliaria",
    "inquilino": "Inquilino",
    "proprietario": "Proprietario",
    "prestador": "Prestador de Serviço"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario_digitado = request.form.get('usuario').lower().strip()
    
    if usuario_digitado in banco_usuarios:
        perfil = banco_usuarios[usuario_digitado]
        
        if perfil == "Imobiliaria":
            return render_template('painel_imobiliaria.html')
        elif perfil == "Inquilino":
            return render_template('painel_inquilino.html')
        elif perfil == "Proprietario":
            return render_template('painel_proprietario.html')
        elif perfil == "Prestador de Serviço":
            return render_template('painel_prestador.html')
    
    return "<h1>Erro: Usuário não encontrado!</h1><br><a href='/'>Voltar para o Login</a>"

@app.route('/cadastro')
def tela_cadastro():
    return render_template('cadastro.html')

@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form.get('nome')
    novo_usuario = request.form.get('novo_usuario').lower().strip()
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    
    banco_usuarios[novo_usuario] = perfil
    
    print("\n----- NOVO USUÁRIO CADASTRADO -----")
    print(f"Nome: {nome}")
    print(f"Login do Usuário: {novo_usuario}")
    print(f"Perfil Atribuído: {perfil}")
    print("-----------------------------------\n")
    
    return f"<h1>{perfil} cadastrado com sucesso!</h1><p>Você já pode voltar e testar o login usando: <b>{novo_usuario}</b></p><br><a href='/'>Ir para o Login</a>"

@app.route('/chamados')
def tela_chamados():
    return render_template('lista_chamados.html')

@app.route('/abrir_chamado')
def tela_abrir_chamado():
    return render_template('abrir_chamado.html')

@app.route('/salvar_chamado', methods=['POST'])
def salvar_chamado():
    titulo_recebido = request.form.get('titulo')
    categoria_recebida = request.form.get('categoria')
    descricao_recebida = request.form.get('descricao')
    
    print("\n----- NOVO CHAMADO RECEBIDO -----")
    print(f"Título: {titulo_recebido}")
    print(f"Categoria: {categoria_recebida}")
    print(f"Descrição: {descricao_recebida}")
    print("---------------------------------\n")
    
    return """
        <h1>Chamado registrado com sucesso!</h1>
        <p>Olhe o terminal do seu VS Code!</p><br>
        <form action='/autenticar' method='POST'>
            <input type='hidden' name='usuario' value='inquilino'>
            <button type='submit' style='padding: 10px; background-color: #555; color: white; border: none; border-radius: 5px; cursor: pointer;'>Voltar ao Painel</button>
        </form>
    """

@app.route('/meus_chamados')
def tela_meus_chamados():
    return render_template('meus_chamados.html')

@app.route('/chamados_estruturais')
def tela_chamados_estruturais():
    return render_template('chamados_estruturais.html')

@app.route('/meus_servicos')
def tela_meus_servicos():
    return render_template('meus_servicos.html')

if __name__ == '__main__':
    app.run(debug=True)