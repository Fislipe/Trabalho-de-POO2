from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class IChamado(ABC):
    @abstractmethod
    def exibir_resumo(self):
        pass


class Chamado(IChamado):
    def __init__(self):
        self.id: str = str(uuid.uuid4())
        self.titulo: str = None
        self.descricao: str = None
        self.categoria: str = None
        self.historico = []
        self.observers = []
        self.__StatusChamado = "Na fila"

    def get_status(self):
        return self.__StatusChamado

    def atualizar_status(self, novo_status):
        # exemplo de validação de status para garantir que apenas valores permitidos sejam usados
        status_validos = ["Na fila", "Em Execução", "Aguardando Aprovação", "Concluído"]
        if novo_status in status_validos:
            self.__StatusChamado = novo_status
            self.historico.append(f"[{datetime.now().strftime('%d/%m %H:%M')}] Status: {novo_status}")
        else:
            raise ValueError(f"O status '{novo_status}' não é permitido.")

    def exibir_resumo(self):
        return f"Chamado: {self.titulo} | Categoria: {self.categoria} | Status: {self.__StatusChamado}"


# aplicacao do padrao builder
class ChamadoBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._chamado = Chamado()
        return self

    def com_titulo(self, titulo):
        self._chamado.titulo = titulo
        return self

    def com_descricao(self, descricao):
        self._chamado.descricao = descricao
        return self

    def com_categoria(self, categoria):
        self._chamado.categoria = categoria
        return self

    def build(self):
        chamado_pronto = self._chamado
        self.historico_inicial = f"Chamado aberto com a categoria: {self._chamado.categoria}"
        chamado_pronto.historico.append(self.historico_inicial)
        self.reset()
        return chamado_pronto


# usando decorator para adicionar funcionalidades extras sem modificar a classe original
class ChamadoDecorator(IChamado):
    def __init__(self, chamado_envolvido: IChamado):
        self._chamado_envolvido = chamado_envolvido

    def exibir_resumo(self):
        return self._chamado_envolvido.exibir_resumo()
    
    def __getattr__(self, nome_atributo):
        return getattr(self._chamado_envolvido, nome_atributo)


class ChamadoUrgenteDecorator(ChamadoDecorator):
    def exibir_resumo(self):
        resumo_original = super().exibir_resumo()
        return f"[URGENTE] {resumo_original}"
    
    def acionar_alerta_imediato(self):
        return f"O chamado '{self.titulo}' requer ação imediata do prestador"