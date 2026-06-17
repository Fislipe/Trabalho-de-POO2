from Classes.usuarios import UsuarioFactory
from Classes.chamado import Chamado

# Fachada para simplificar a chamada das coisas no app.py
class SistemaImobiliarioFacade:
    @staticmethod
    def registrar_novo_usuario(perfil, nome, documento, email, senha):
        try:
            novo_usuario = UsuarioFactory.criar_usuario(perfil, nome, documento, email, senha)
            return novo_usuario
        except Exception as e:
            raise ValueError(f"Erro no cadastro: {str(e)}")

    @staticmethod
    def abrir_novo_chamado(titulo, descricao, categoria):
        novo_chamado = Chamado(titulo, descricao, categoria)
        return novo_chamado
        
    @staticmethod
    def atualizar_andamento_chamado(chamado):
        chamado.avancar_status()
        return chamado.get_status()