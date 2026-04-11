from fastapi import HTTPException, Depends, status
from jose import ExpiredSignatureError, jwt, JWTError
import logging
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from src.api.schemas.auth_schema import AuthLoginRequest
from src.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.repositories.usuario_repository import consultar_usuario_por_email_repository, consultar_usuario_por_id_repository

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def gerar_hash_senha(senha: str) -> str:
    if not isinstance(senha, str) or not senha.strip():
        raise ValueError("Senha inválida.")

    return password_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    if not isinstance(senha, str) or not senha.strip():
        raise ValueError("Senha inválida.")

    if not isinstance(senha_hash, str) or not senha_hash.strip():
        raise ValueError("Hash de senha inválido.")

    try:
        return password_context.verify(senha, senha_hash)
    except Exception:
        
        return False


def login_service(dados_login: AuthLoginRequest):
    usuario_auth = consultar_usuario_por_email_repository(dados_login.email)

    if not usuario_auth:
        logger.warning("Falha de login - usuário Não encontrado - email=%s", dados_login.email)
        raise ValueError("Não existe usuario com este email.")
    
    senha_valida = verificar_senha(
        dados_login.senha,
        usuario_auth.senha_hash,
    )

    if not senha_valida:
        logger.warning("Falha de login - senha inválida - email=%s usuario_id=%s", usuario_auth.email, usuario_auth.id)
        raise ValueError("Email ou senha inválidos.")
    
    access_token = criar_access_token(
        data={
            "sub": str(usuario_auth.id),
            "email": usuario_auth.email,
            "type": "access"
        }
    )

    refresh_token = criar_refresh_token(usuario_auth.id)
    logger.info("Login realizado com sucesso - usuario_id=%s email=%s", usuario_auth.id, usuario_auth.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




def criar_access_token(data: dict) -> str:
    dados_token = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": expire})

    return jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        sub = payload.get("sub")
        token_type = payload.get("type")

        if sub is None:
            logger.warning("Token inválido - claim 'sub' ausente")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.",)
        
        if token_type != "access":
            logger.warning("Token inválido - tipo de token inválido - type=%s", token_type)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.",)

        usuario_id = int(sub)
        usuario = consultar_usuario_por_id_repository(usuario_id)

        if usuario is None:
            logger.warning("Token inválido - usuário não encontrado - usuario_id=%s", usuario_id)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.",)

        return usuario

    except JWTError:
        logger.warning("Token inválido - falha ao decodificar JWT")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.",)
    except ValueError:
        logger.warning("Token inválido - sub em formato inválido")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.",)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro inesperado ao validar token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.",)


def criar_refresh_token(usuario_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=15)

    payload = {
        "sub": str(usuario_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def refresh_token_service(refresh_token: str, ip: str):
    logger.info("Tentativa de refresh token - ip=%s", ip)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        token_type = payload.get("type")
        sub = payload.get("sub")

        if token_type != "refresh":
            logger.warning("Falha no refresh - tipo inválido - ip=%s", ip)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido.")

        if sub is None:
            logger.warning("Falha no refresh - claim sub ausente - ip=%s", ip)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido.")

        user_id = int(sub)

        novo_access_token = criar_access_token(
            data={
                "sub": str(user_id),
                "type": "access"
            }
        )

        logger.info("Refresh realizado com sucesso - usuario_id=%s ip=%s", user_id, ip)

        return {
            "access_token": novo_access_token,
            "token_type": "bearer"
        }

    except ExpiredSignatureError:
        logger.warning("Falha no refresh - token expirado - ip=%s", ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expirado.")

    except JWTError:
        logger.warning("Falha no refresh - erro ao decodificar JWT - ip=%s", ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido.")

    except ValueError:
        logger.warning("Falha no refresh - sub inválido - ip=%s", ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido.")

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro inesperado ao renovar token - ip=%s", ip)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")