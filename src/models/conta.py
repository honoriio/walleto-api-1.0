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
    
    