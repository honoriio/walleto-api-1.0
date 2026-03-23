import pytest


# Quem me deu essa dica foi o chat gpt, achei interessante e decidi usar. ecomiza na repetição de codigos e deixa as funções de tests mais limpas. 
@pytest.fixture
def simular_input(monkeypatch):
    def _simular(entradas):
        iter_entradas = iter(entradas)
        monkeypatch.setattr("builtins.input", lambda _: next(iter_entradas))
    return _simular