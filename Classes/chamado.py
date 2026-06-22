from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class EstadoChamado(ABC):
    @abstractmethod
    def proximo_estado(self, chamado):
        pass

    @abstractmethod
    def __str__(self):
        pass

# RE ADICIONADO: Estado inicial do ciclo de vida
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
        if not chamado.confirmado_pelo_inquilino:
            raise ValueError("O inquilino precisa confirmar o reparo.")
        chamado.estado = EstadoEncerrado()
        chamado.adicionar_historico("Status alterado para: Encerrado")
        
    def __str__(self): return "Resolvido"

class EstadoEncerrado(EstadoChamado):
    def proximo_estado(self, chamado):
        raise ValueError("Chamado já encerrado.")
    def __str__(self): return "Encerrado"


class Chamado:
    def __init__(self, titulo, descricao, categoria):
        self.id = str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.confirmado_pelo_inquilino = False

        if categoria.strip().lower() == "estrutural":
            self.responsavel = "Proprietário"
        else:
            self.responsavel = "Imobiliária"

        self.historico = []
        self.estado = EstadoAberto() 
        self.adicionar_historico(f"Chamado aberto na categoria: {self.categoria}")
        self.prestador = None

    def confirmar_reparo(self):
        self.confirmado_pelo_inquilino = True
        self.adicionar_historico("Inquilino confirmou a execução do reparo.")

    def adicionar_historico(self, mensagem):
        self.historico.append(
            f"[{datetime.now().strftime('%d/%m %H:%M')}] {mensagem}"
        )

    def avancar_status(self):
        self.estado.proximo_estado(self)

    def get_status(self):
        return str(self.estado)

    def exibir_resumo(self):
        return f"Chamado: {self.titulo} | Categoria: {self.categoria} | Status: {self.get_status()}"
    
    def atribuir_prestador(self, prestador):
        self.prestador = prestador

    def definir_estado(self, status_atual):
        if status_atual == "Aberto": self.estado = EstadoAberto()
        elif status_atual == "Em Análise": self.estado = EstadoEmAnalise()
        elif status_atual == "Em Execução": self.estado = EstadoEmExecucao()
        elif status_atual == "Resolvido": self.estado = EstadoResolvido()
        elif status_atual == "Encerrado": self.estado = EstadoEncerrado()