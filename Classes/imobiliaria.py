from abc import abstractmethod
import uuid

class imobiliaria:
    def __init__(self, nome, cnpj, endereco):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco