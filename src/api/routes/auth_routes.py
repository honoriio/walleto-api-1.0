import logging
from fastapi import Request
from src.core.rate_limiter import limiter
from fastapi import APIRouter, HTTPException, Depends, logger
from src.api.schemas.auth_schema import AuthLoginRequest, AuthTokenResponse, AuthMeResponse
from src.services.auth_service import login_service, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=AuthTokenResponse, status_code=200)
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
    

@router.get("/me", response_model=AuthMeResponse, status_code=200)
@limiter.limit("5/minute")
def buscar_usuario_logado_api(request: Request, current_user=Depends(get_current_user)):
    logger.info("Requisição de usuário autenticado - usuario_id=%s", current_user.id)

    try:
        return current_user

    except Exception:
        logger.exception(
            "Erro ao buscar usuário autenticado - usuario_id=%s", current_user.id,)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")