from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Gasto:
    nome: str
    valor: Decimal
    categoria: str
    descricao: str
    data: date
    id: int | None = None

