from pydantic import BaseModel
from datetime import date


class UsuarioCreateRequest(BaseModel):
    nome: str
    email: str 
    data_nascimento: date 
    sexo: str
    senha: str


class UsuarioResponse(BaseModel):
    nome: str
    email: str 
    data_nascimento: date 
    sexo:str


class UsuarioListResponse(BaseModel):
    usuario: list[UsuarioResponse]


class UsuarioUpdateRequest(BaseModel):
    nome: str | None = None
    email: str | None = None
    data_nascimento: date | None = None
    sexo: str | None = None


