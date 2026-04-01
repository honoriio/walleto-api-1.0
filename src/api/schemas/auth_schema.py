from pydantic import BaseModel, EmailStr

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

class RefreshTokenRequest():
    pass


class PasswordResetRequest():
    pass

