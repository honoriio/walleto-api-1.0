import logging
from fastapi import Request
from src.core.rate_limiter import limiter
from fastapi import APIRouter, HTTPException, Depends, logger
from src.api.schemas.auth_schema import AuthLoginRequest, AuthTokenResponse, AuthMeResponse, RefreshTokenRequest, RefreshTokenResponse
from src.services.auth_service import login_service, get_current_user, refresh_token_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=AuthTokenResponse, status_code=200, summary="Realizar login", description="Autentica o usuário e retorna access token e refresh token.",)
@limiter.limit("5/minute")
def login_usuario_api(request: Request, dados_login: AuthLoginRequest):
    logger.info("Login iniciado - email=%s", dados_login.email)
    try:
        return login_service(dados_login)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))
    except Exception:
        logger.exception("Erro inesperado na rota de login - email=%s", dados_login.email)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    

@router.get("/me", response_model=AuthMeResponse, status_code=200,  summary="Obter usuário autenticado", description="Retorna os dados do usuário autenticado a partir do token JWT.")
@limiter.limit("5/minute")
def buscar_usuario_logado_api(request: Request, current_user=Depends(get_current_user)):
    logger.info("Requisição de usuário autenticado - usuario_id=%s", current_user.id)

    try:
        return current_user

    except Exception:
        logger.exception(
            "Erro ao buscar usuário autenticado - usuario_id=%s", current_user.id,)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    

@router.post("/refresh", response_model=RefreshTokenResponse, status_code=200, summary="Refresh access token", description=(
    "Gera um novo access token utilizando um refresh token válido. "
    "O refresh token deve ser enviado no corpo da requisição. "
    "Caso o token seja inválido ou expirado, a requisição será rejeitada."
))

@limiter.limit("5/hour")
def refresh_token_api(request: Request, data: RefreshTokenRequest):
    logger.info("Tentativa de refresh token")

    try:
        ip = request.client.host if request.client else "desconhecido"
        return refresh_token_service(data.refresh_token, ip)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))
    except Exception:
        logger.exception("Erro inesperado na rota de refresh")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")