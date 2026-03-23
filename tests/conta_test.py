import pytest
from src.models.conta import Conta


"""Eu acredito que os testes da classe Conta e seus metodos estejam ok e finalizados. """
def test_deposito_positivo(): # --> Criado para testar depositos de valores na conta. 
    conta = Conta(1000)
    resultado = conta.depositar(500, "Depósito")
    
    # Saldo deve aumentar
    assert conta.saldo == 1500
    # Deve retornar True
    assert resultado is True
    # Transação registrada corretamente
    assert conta.transacoes[-1] == {
        "tipo": "entrada",
        "valor": 500,
        "descricao": "Depósito"
    }

def test_deposito_zero_ou_negativo(): # Testa se a função de deposito trata bem a questão de depositos com valores menores ou igual a zero
    conta = Conta(1000)
    
    # Depósito negativo
    with pytest.raises(ValueError):
        conta.depositar(-100)
    
    # Depósito zero
    with pytest.raises(ValueError):
        conta.depositar(0)


def test_saldo_total(): # Testa se a função de saldo total, de fato retorna o saldo da conta real.
    conta = Conta(1000)

    # Antes de qualquer operação, vamos adicionar o valor
    assert conta.saldo_total() == 1000


    # Apos o deposito 
    conta.depositar(500)
    assert conta.saldo_total() == 1500 

    # Não criarei o teste de saque, pois o programa e apenas um gestor de gastos, o mesmo tera uma função que ira abater o valor das dividas 
    # No saldo posivo da conta do cliente, afim de gerar um relatorio de renda positiva e gastos. 


def test_obter_transacoes():
    conta = Conta(1000)
    conta.depositar(200)

    transacoes = conta.obter_transacoes()

    # Verificação se a transação foi registrada.
    assert transacoes == [{"tipo": "entrada", "valor": 200, "descricao": "Depósito"}]
    
    # Modificando a lista retornada não deve alterar self.transacoes
    transacoes.append({"tipo":"saida","valor":100,"descricao":"Saque"})
    assert conta.transacoes == [{"tipo": "entrada", "valor": 200, "descricao": "Depósito"}]
    