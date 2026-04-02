from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Gasto:
    nome: str
    valor: Decimal
    categoria: str
    descricao: str
    data: date
    usuario_id: int
    id: Optional[int] = None
