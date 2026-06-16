from abc import ABC, abstractmethod
import uuid


class usuarios(ABC):
    def __init__(self, nome, email, senha, perfil):
        self.id:str = str(uuid.uuid4())
        self.nome:str = nome
        self.email:str = email
        self.__senha:str = senha
        self.perfil = perfil
        



class cliente(usuarios):
    def __init__(self, nome, cpf, email, senha, perfil):
        super().__init__(nome, cpf, email, senha, perfil)
        self.cpf = cpf

class imobiliaria(usuarios):
    def __init__(self, nome, cnpj, email, senha, perfil):
        super().__init__(nome, email, senha, perfil)
        self.cnpj = cnpj

class forncedor(usuarios):
    def __init__(self, nome, cnpj, email, senha, perfil):
        super().__init__(nome, email, senha, perfil)
        self.cnpj = cnpj
