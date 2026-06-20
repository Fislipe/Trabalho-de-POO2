from Classes.usuarios import UsuarioFactory
from Classes.chamado import Chamado
from supabase import create_client, Client

SUPABASE_URL = "https://aawotiynbpxgykxzlyux.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhd290aXluYnB4Z3lreHpseXV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE2NDAzMzAsImV4cCI6MjA5NzIxNjMzMH0.ntk2VmlVvUHphWyZCMXx1_Ng5jaVPCuy0yUQmvwpshY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SistemaImobiliarioFacade:
    @staticmethod
    def registrar_novo_usuario(perfil, nome, documento, email, senha):
        try:
            novo_usuario = UsuarioFactory.criar_usuario(perfil, nome, documento, email, senha)
            
            dados = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "perfil": novo_usuario.obter_perfil()
            }
            supabase.table("usuarios").insert(dados).execute()
            
            return novo_usuario
        except Exception as e:
            raise ValueError(f"Erro no cadastro: {str(e)}")

    @staticmethod
    def autenticar_usuario(email, senha_digitada):
        resposta = supabase.table("usuarios").select("*").eq("email", email).execute()
        usuarios_encontrados = resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
        
        if usuarios_encontrados:
            dados_db = usuarios_encontrados[0]
            
            usuario_obj = UsuarioFactory.criar_usuario(
                perfil=dados_db['perfil'],
                nome=dados_db['nome'],
                documento=dados_db['email'],
                email=dados_db['email'],
                senha=dados_db['senha']
            )
            
            if usuario_obj.validar_senha(senha_digitada):
                return usuario_obj
                
        return None

    @staticmethod
    def abrir_novo_chamado(titulo, descricao, categoria):
        novo_chamado = Chamado(titulo, descricao, categoria)
        return novo_chamado
        
    @staticmethod
    def atualizar_andamento_chamado(chamado):
        chamado.avancar_status()
        return chamado.get_status()