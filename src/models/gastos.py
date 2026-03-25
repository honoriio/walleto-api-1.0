from decimal import Decimal

class Gasto:
    def __init__(
        self,
        nome: str,
        valor: Decimal,
        categoria: str,
        descricao: str,
        data: str,
        id: int | None = None,
    ):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.categoria = categoria
        self.descricao = descricao
        self.data = data