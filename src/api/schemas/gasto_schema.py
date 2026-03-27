from pydantic import BaseModel
from datetime import date
from decimal import Decimal



class GastoCreateRequest(BaseModel):
    nome: str
    valor: Decimal
    categoria: str
    data: date | None = None
    descricao: str | None = None


class GastoResponse(BaseModel):
    id: int
    nome: str
    valor: Decimal
    categoria: str
    data: date
    descricao: str | None = None


class GastoListResponse(BaseModel):
    gastos: list[GastoResponse]
    total: Decimal



class GastoUpdateRequest(BaseModel):
    nome: str | None = None
    valor: Decimal | None = None
    categoria: str | None = None
    data: date | None = None
    descricao: str | None = None
