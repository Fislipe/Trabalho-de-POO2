from abc import abstractmethod
import uuid

class usuarios:
    def __init__(self, nome, cpf, email, senha):
        self.id:str = str(uuid.uuid4())
        self.nome:str = nome
        self.cpf:str = cpf
        self.email:str = email
        self.__senha:str = senha