from abc import ABC, abstractmethod
import uuid
from datetime import datetime

# Controle de estados usando State
class EstadoChamado(ABC):
    @abstractmethod
    def proximo_estado(self, chamado):
        pass

    @abstractmethod
    def __str__(self):
        pass

class EstadoAberto(EstadoChamado):
    def proximo_estado(self, chamado):
        chamado.estado = EstadoEmAnalise()
        chamado.adicionar_historico("Status alterado para: Em Análise")
    def __str__(self): return "Aberto"

class EstadoEmAnalise(EstadoChamado):
    def proximo_estado(self, chamado):
        chamado.estado = EstadoEmExecucao()
        chamado.adicionar_historico("Status alterado para: Em Execução")
    def __str__(self): return "Em Análise"

class EstadoEmExecucao(EstadoChamado):
    def proximo_estado(self, chamado):
        chamado.estado = EstadoResolvido()
        chamado.adicionar_historico("Status alterado para: Resolvido")
    def __str__(self): return "Em Execução"

class EstadoResolvido(EstadoChamado):
    def proximo_estado(self, chamado):
        chamado.estado = EstadoEncerrado()
        chamado.adicionar_historico("Status alterado para: Encerrado")
    def __str__(self): return "Resolvido"

class EstadoEncerrado(EstadoChamado):
    def proximo_estado(self, chamado):
        raise ValueError("Chamado ja encerrado.")
    def __str__(self): return "Encerrado"


class Chamado:
    def __init__(self, titulo, descricao, categoria):
        self.id = str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.historico = []
        self.estado = EstadoAberto() 
        self.adicionar_historico(f"Chamado aberto na categoria: {self.categoria}")

    def adicionar_historico(self, mensagem):
        self.historico.append(f"[{datetime.now().strftime('%d/%m %H:%M')}] {mensagem}")

    def avancar_status(self):
        self.estado.proximo_estado(self)

    def get_status(self):
        return str(self.estado)

    def exibir_resumo(self):
        return f"Chamado: {self.titulo} | Categoria: {self.categoria} | Status: {self.get_status()}"