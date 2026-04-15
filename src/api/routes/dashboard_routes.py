import os

from fastapi import APIRouter, Depends, HTTPException
import logging

from fastapi.responses import RedirectResponse
from requests.compat import quote, urljoin
from src.infrastructure.dashboard.streamlit_dashboard import encerrar_dashboard, obter_status_dashboard
from src.models.usuario import Usuario
from fastapi import Request
from src.core.rate_limiter import limiter
from src.services.auth_service import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/iniciar", include_in_schema=True)
@limiter.limit("10/hour")
def iniciar_dashboard_api(
    request: Request,
    current_user: Usuario = Depends(get_current_user)
):
    logger.info("Redirecionando para dashboard | usuario_id=%s", current_user.id)

    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Não autenticado")

        token = auth_header.replace("Bearer ", "").strip()

        base_url = os.getenv("DASHBOARD_URL").rstrip("/")

        if not base_url:
            raise HTTPException(status_code=500, detail="DASHBOARD_URL não configurada")

        # garante formato correto da URL
        dashboard_url = f"{base_url}/dashboard?token={token}"

        logger.info(
            "Redirecionando usuário para dashboard_url=%s user_id=%s",
            dashboard_url,
            current_user.id
        )

        return RedirectResponse(
            url=dashboard_url,
            status_code=303,
            headers={"X-Dashboard-URL": dashboard_url}
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Erro ao iniciar dashboard | usuario_id=%s",
            current_user.id
        )
        raise HTTPException(status_code=500, detail="Erro interno ao iniciar dashboard.")


@router.post("/encerrar", summary="Encerra o dashboard do usuário",
description="""
Finaliza a execução do dashboard ativo do usuário autenticado.
""", include_in_schema=False)

@limiter.limit("10/hour", )
def encerrar_dashboard_api(request: Request, current_user: Usuario = Depends(get_current_user)):
    logger.info("Encerramento de dashboard solicitado | usuario_id=%s", current_user.id)

    try:
        resultado = encerrar_dashboard(current_user.id)

        logger.info("Dashboard encerrado com sucesso | usuario_id=%s", current_user.id)
        return resultado

    except Exception:
        logger.exception("Erro inesperado ao encerrar dashboard | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Erro interno ao encerrar dashboard.")


@router.get("/status", summary="Obtém o status do dashboard",
description="""
Retorna o estado atual do dashboard do usuário autenticado.
""", include_in_schema=False)

@limiter.limit("10/hour")
def status_dashboard_api(request: Request, current_user: Usuario = Depends(get_current_user)):
    try:
        return obter_status_dashboard(current_user.id)

    except Exception:
        logger.exception("Erro ao obter status do dashboard | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500,detail="Erro ao obter status do dashboard.")