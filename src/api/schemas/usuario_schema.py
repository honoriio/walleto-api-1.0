from pydantic import BaseModel
from datetime import date


class UsuarioCreateRequest(BaseModel):
    nome: str
    email: str 
    data_nascimento: date 
    sexo: str
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str 
    data_nascimento: date 
    sexo:str


class UsuarioListResponse(BaseModel):
    usuarios: list[UsuarioResponse]
    quantidade: int


class UsuarioUpdateRequest(BaseModel):
    nome: str | None = None
    email: str | None = None
    data_nascimento: date | None = None
    sexo: str | None = None


