from abc import ABC, abstractmethod
import uuid

class Usuario(ABC):
    def __init__(self, nome, email, senha, perfil):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.__senha = senha
        self.perfil = perfil
        
    def validar_senha(self, senha_digitada):
        return self.__senha == senha_digitada

    def obter_perfil(self):
        return self.perfil

class Inquilino(Usuario):
    def __init__(self, nome, documento, email, senha):
        super().__init__(nome, email, senha, "Inquilino")
        self.cpf = documento

class Proprietario(Usuario):
    def __init__(self, nome, documento, email, senha):
        super().__init__(nome, email, senha, "Proprietário")
        self.cpf_cnpj = documento

class Imobiliaria(Usuario):
    def __init__(self, nome, documento, email, senha):
        super().__init__(nome, email, senha, "Imobiliária")
        self.cnpj = documento

class PrestadorServico(Usuario):
    def __init__(self, nome, documento, email, senha):
        super().__init__(nome, email, senha, "Prestador de Serviço")
        self.cnpj_cpf = documento

class UsuarioFactory:
    @staticmethod
    def criar_usuario(perfil, nome, documento, email, senha):
        perfil_limpo = perfil.strip().lower()
        
        if perfil_limpo == "inquilino":
            return Inquilino(nome, documento, email, senha)
        elif perfil_limpo in ["proprietario", "proprietário"]:
            return Proprietario(nome, documento, email, senha)
        elif perfil_limpo in ["imobiliaria", "imobiliária"]:
            return Imobiliaria(nome, documento, email, senha)
        elif perfil_limpo in ["prestador de serviço", "prestador de servico", "prestador"]:
            return PrestadorServico(nome, documento, email, senha)
        else:
            raise ValueError(f"Perfil '{perfil}' inválido.")