from pydantic import BaseModel, EmailStr
from datetime import date

class AuthLoginRequest(BaseModel):
    email: EmailStr
    senha: str


class AuthLoginResponse(BaseModel):
    mensagem: str
    usuario_id: int
    email: EmailStr


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str

class AuthMeResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_nascimento: date
    sexo: str

class RefreshTokenRequest():
    pass


class PasswordResetRequest():
    pass

