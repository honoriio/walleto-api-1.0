from pydantic import BaseModel, EmailStr
from datetime import date

class AuthLoginRequest(BaseModel):
    email: EmailStr
    senha: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class AuthLoginResponse(BaseModel):
    mensagem: str
    usuario_id: int
    email: EmailStr


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AuthMeResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_nascimento: date
    sexo: str


class PasswordResetRequest(BaseModel): # ainda precisamos criar isso aqui 
    pass

