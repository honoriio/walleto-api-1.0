from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional



class GastoCreateRequest(BaseModel):
    nome: str
    valor: Decimal
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    data: Optional[date] = None


class GastoResponse(BaseModel):
    id: int
    nome: str
    valor: Decimal
    categoria: Optional[str]
    descricao: Optional[str]
    data: date
    usuario_id: int


class GastoListResponse(BaseModel):
    gastos: list[GastoResponse]
    total: Decimal
    quantidade: int



class GastoUpdateRequest(BaseModel):
    nome: str | None = None
    valor: Decimal | None = None
    categoria: str | None = None
    data: date | None = None
    descricao: str | None = None
