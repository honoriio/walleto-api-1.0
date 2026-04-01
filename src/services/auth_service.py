from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from src.api.schemas.auth_schema import AuthLoginRequest
from src.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.repositories.usuario_repository import consultar_usuario_por_email_repository, consultar_usuario_por_id_repository



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def gerar_hash_senha(senha: str) -> str:
    return password_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_context.verify(senha, senha_hash)


def login_service(dados_login: AuthLoginRequest):
    usuario_auth = consultar_usuario_por_email_repository(dados_login.email)

    if not usuario_auth:
        raise ValueError("Não existe usuario com este email.")
    
    senha_valida = verificar_senha(
        dados_login.senha,
        usuario_auth.senha_hash,
    )

    if not senha_valida:
        raise ValueError("Email ou senha inválidos.")
    
    access_token = criar_access_token(
        data={
            "sub": str(usuario_auth.id),
            "email": usuario_auth.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }




def criar_access_token(data: dict) -> str:
    dados_token = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": expire})

    return jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: str = Depends(oauth2_scheme)):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")

        if sub is None:
            raise credenciais_invalidas

        usuario_id = int(sub)

    except (JWTError, ValueError):
        raise credenciais_invalidas

    usuario = consultar_usuario_por_id_repository(usuario_id)

    if usuario is None:
        raise credenciais_invalidas

    return usuario
