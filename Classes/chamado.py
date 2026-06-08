from abc import abstractmethod
import uuid

class chamado:
    def __init__(self, titulo, descricao, categoria, historico, StatusChamado="Na fila", observers=None):
        self.id:str = str(uuid.uuid4())
        self.titulo:str = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.historico = historico
        self.StatusChamado = StatusChamado
        self.observers = observers