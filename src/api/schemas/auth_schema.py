from pydantic import BaseModel, EmailStr

class AuthLoginRequest(BaseModel):
    email: EmailStr
    senha: str


class AuthLoginResponse(BaseModel):
    mensagem: str
    usuario_id: int
    email: EmailStr


class TokenResponse():
    pass


class RefreshTokenRequest():
    pass


class PasswordResetRequest():
    pass

