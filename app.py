from flask import Flask, render_template, request
from supabase import create_client, Client
from Classes.usuarios import UsuarioFactory

app = Flask(__name__)

SUPABASE_URL = "https://aawotiynbpxgykxzlyux.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhd290aXluYnB4Z3lreHpseXV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE2NDAzMzAsImV4cCI6MjA5NzIxNjMzMH0.ntk2VmlVvUHphWyZCMXx1_Ng5jaVPCuy0yUQmvwpshY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario_digitado = request.form.get('usuario').strip()
    senha_digitada = request.form.get('senha')
    
    try:
        # busca no supa se tem um usuario com o email digitado, e pega os dados dele
        resposta = supabase.table("usuarios").select("*").eq("email", usuario_digitado).execute()
        usuarios_encontrados = resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
        
        if usuarios_encontrados:
            dados_db = usuarios_encontrados[0]
            
            # usa a fabrica para montar o objeto com os dados reais
            usuario_objeto = UsuarioFactory.criar_usuario(
                perfil=dados_db['perfil'],
                nome=dados_db['nome'],
                documento=dados_db['email'], # Email provisório como documento
                email=dados_db['email'],
                senha=dados_db['senha']
            )
            
            # proprio objeto confirma a senha e diz qual é o painel dele
            if usuario_objeto.validar_senha(senha_digitada):
                perfil = usuario_objeto.obter_perfil()
                
                if perfil == "imobiliaria" or perfil == "Imobiliaria":
                    return render_template('painel_imobiliaria.html')
                elif perfil == "Inquilino":
                    return render_template('painel_inquilino.html')
                elif perfil == "Proprietario":
                    return render_template('painel_proprietario.html')
                elif perfil == "Prestador de Serviço":
                    return render_template('painel_prestador.html')
        
        
        return render_template('login.html', erro="Usuário ou senha incorretos!")
        
    except Exception as e:
        # se der problema no banco de dados, também avisa na mesma tela
        return render_template('login.html', erro="Erro de conexão com o banco de dados.")


@app.route('/cadastro')
def tela_cadastro():
    return render_template('cadastro.html')


@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form.get('nome')
    novo_usuario = request.form.get('novo_usuario').strip()
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    
    try:
        usuario_obj = UsuarioFactory.criar_usuario(
            perfil=perfil,
            nome=nome,
            documento=novo_usuario,
            email=novo_usuario,
            senha=senha
        )
        
        # fazer esse metodo de salvar dentro da classe para manter a lógica de persistência encapsulada
        usuario_obj.salvar_no_banco(supabase)
        
        return f"""
            <h1>{perfil} cadastrado com sucesso!</h1>
            <p>Acesse o sistema com o novo usuário: <b>{novo_usuario}</b></p><br>
            <form action='/autenticar' method='POST'>
                <input type='hidden' name='usuario' value='imobiliaria@gmail.com'>
                <input type='hidden' name='senha' value='123'>
                <button type='submit' style='padding: 10px; background-color: #555; color: white; border: none; border-radius: 5px; cursor: pointer;'>Voltar ao Painel da Imobiliária</button>
            </form>
        """
    except Exception as e:
        return f"<h1>Erro ao salvar usuário:</h1><p>{str(e)}</p><br><a href='/cadastro'>Tentar Novamente</a>"


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
    
    return """
        <h1>Chamado registrado com sucesso!</h1>
        <form action='/autenticar' method='POST'>
            <input type='hidden' name='usuario' value='inquilino'>
            <input type='hidden' name='senha' value='123'>
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