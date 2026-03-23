"""A classe conta e resposanvel pelo valor que o usuario vai informar para poder ver o que gastou com base no seu salario, para poder gerar relatorios de gastos etc. 
vai funcionar assim,  o usuario informa sua renda mensal, salario fixo, renda extra, renda de envestimentos etc.. a estrutura vai ser mais ou menos assim

Valor: 200
Tipo: despesa
Categoria: alimentação
Descrição: mercado

e o valor da conta sera abatido os gastos que o mesmo teve mensal, a ideia futura e separar o que foi gasto no debito, do que foi gasto no credito ou a prazo. 
e gerar  um relatorio para o nosso usario.   a classe conta vai tomar conta de entradas e saidas dos valores que forem debitados do valor inserido na conta do usuario
atuamente, somente deixamos marcado e damos um total de gastos para o usuario, o mesmo, podera manter o uso assim se quiser ou optar por informar os saldos positivos 
que o mesmo recebe durante o mês."""


class Conta:  # --> Acho que irei mudar essa classe, somente para aceitar um unico valor e aceitar uma descrição e uma categoria. 
    def __init__(self, salario):
        self.saldo = salario
        self.transacoes = []
        


    def depositar(self, valor, descricao= "Depósito"):

        if valor <= 0:
            raise ValueError("O valor não pode ser igual ou menor que 0.")

        self.saldo += valor

        transacao = {
            "tipo": "entrada",
            "valor": valor,
            "descricao": descricao
        }

        self.transacoes.append(transacao)

        return True
    


    def saldo_total(self):
        return self.saldo 
    

    def obter_transacoes(self):
        return list(self.transacoes)

    

    def __str__(self):
        return f"Saldo total: R${self.saldo_total():.2f}"
    
    