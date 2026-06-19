import pytest
from Classes.chamado import Chamado

def test_transicao_estados_chamado():
    chamado = Chamado("Vazamento", "Cano furado na cozinha", "Hidraulica")
    assert chamado.get_status() == "Aberto"

    chamado.avancar_status()
    assert chamado.get_status() == "Em Análise"

    chamado.avancar_status()
    chamado.avancar_status()
    chamado.avancar_status() 
    assert chamado.get_status() == "Encerrado"

    with pytest.raises(ValueError, match="Chamado ja encerrado."):
        chamado.avancar_status()