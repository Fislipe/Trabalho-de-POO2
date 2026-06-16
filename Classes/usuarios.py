from abc import ABC, abstractmethod
import uuid

class usuarios(ABC):
    def __init__(self, nome, email, senha, perfil):
        self.id:str = str(uuid.uuid4())
        self.nome:str = nome
        self.email:str = email
        self.__senha:str = senha
        self.perfil = perfil
        
    # metodos provisórios para o app.py conseguir testar o login
    def validar_senha(self, senha_digitada):
        return self.__senha == senha_digitada

    def obter_perfil(self):
        return self.perfil


class cliente(usuarios):
    def __init__(self, nome, cpf, email, senha, perfil):
        super().__init__(nome, email, senha, perfil)
        self.cpf = cpf

class imobiliaria(usuarios):
    def __init__(self, nome, cnpj, email, senha, perfil):
        super().__init__(nome, email, senha, perfil)
        self.cnpj = cnpj

class fornecedor(usuarios):
    def __init__(self, nome, cnpj, email, senha, perfil):
        super().__init__(nome, email, senha, perfil)
        self.cnpj = cnpj

#fabrica provisoria pra conseguir rodar o app.py, depois implementar a logica correta aqui dentro
class UsuarioFactory:
    @staticmethod
    def criar_usuario(perfil, nome, documento, email, senha):
        #porfavor, façam a logica de criar o objeto certo dependendo do perfil, isso é um exemplo provisório
        return imobiliaria(nome, documento, email, senha, perfil)