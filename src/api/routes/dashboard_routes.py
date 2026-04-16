from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from slowapi import Limiter

from src.models.usuario import Usuario
from src.services.auth_service import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/dados")
def obter_dados_dashboard(
    current_user: Usuario = Depends(get_current_user)
):
    from src.services.dashboard_service import obter_gastos_dashboard

    try:
        dados = obter_gastos_dashboard(current_user.id)
        return {"gastos": dados}

    except Exception:
        logger.exception("Erro ao obter dados do dashboard")
        raise HTTPException(status_code=500, detail="Erro interno")


@router.post("/iniciar")
def iniciar_dashboard_api(
    request: Request,
    current_user: Usuario = Depends(get_current_user)
):
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=401, detail="Não autenticado")

        token = auth_header.replace("Bearer ", "")

        dashboard_url = f"https://SEU-DASHBOARD.onrender.com/?token={token}"

        logger.info(
            "Inicialização de dashboard solicitada | usuario_id=%s",
            current_user.id
        )

        return {
            "dashboard_url": dashboard_url,
            "token": token,
            "user_id": current_user.id
        }

    except HTTPException:
        raise

    except Exception:

        logger.exception("Erro inesperado ao iniciar dashboard | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Erro interno ao iniciar dashboard.")

@router.post("/encerrar", summary="Encerra o dashboard do usuário",
description="""
Finaliza a execução do dashboard ativo do usuário autenticado.
""", include_in_schema=False)

@Limiter.limit("10/hour", )
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

        logger.exception("Erro ao iniciar dashboard")
        raise HTTPException(status_code=500, detail="Erro interno")


        logger.exception("Erro ao iniciar dashboard")
        raise HTTPException(status_code=500, detail="Erro interno")

    
    