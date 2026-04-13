from fastapi import APIRouter, Depends, HTTPException
import logging
from src.infrastructure.dashboard.streamlit_dashboard import encerrar_dashboard, obter_status_dashboard
from src.models.usuario import Usuario
from fastapi import Request
from src.core.rate_limiter import limiter
from src.services.auth_service import get_current_user
from src.services.dashboard_service import iniciar_dashboard_com_exportacao

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/iniciar", summary="Inicia o dashboard do usuário",
description="""
Inicializa o dashboard do usuário autenticado após preparar os dados necessários.

Pode retornar erro caso não existam dados ou ocorra falha durante a inicialização.
""")
@limiter.limit("10/hour")
def iniciar_dashboard_api(request: Request, current_user: Usuario = Depends(get_current_user)):
    logger.info("Inicialização de dashboard solicitada | usuario_id=%s", current_user.id,)

    try:
        resultado = iniciar_dashboard_com_exportacao(current_user.id)

        logger.info("Dashboard iniciado com sucesso | usuario_id=%s", current_user.id,)
        return resultado

    except FileNotFoundError as erro:
        logger.warning("Falha ao iniciar dashboard | arquivo de exportação não encontrado | usuario_id=%s | erro=%s", current_user.id, erro,)
        raise HTTPException(status_code=404, detail=str(erro))

    except ValueError as erro:
        logger.warning("Falha ao iniciar dashboard por validação | usuario_id=%s | erro=%s", current_user.id, erro,)
        raise HTTPException(status_code=400, detail=str(erro))

    except RuntimeError as erro:
        logger.warning("Falha ao iniciar dashboard | erro de execução | usuario_id=%s | erro=%s", current_user.id, erro,)
        raise HTTPException(status_code=500, detail=str(erro))

    except Exception:
        logger.exception("Erro inesperado ao iniciar dashboard | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Erro interno ao iniciar dashboard.")


@router.post("/encerrar", summary="Encerra o dashboard do usuário",
description="""
Finaliza a execução do dashboard ativo do usuário autenticado.
""")

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
""")

@limiter.limit("10/hour")
def status_dashboard_api(request: Request, current_user: Usuario = Depends(get_current_user)):
    try:
        return obter_status_dashboard(current_user.id)

    except Exception:
        logger.exception("Erro ao obter status do dashboard | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500,detail="Erro ao obter status do dashboard.")