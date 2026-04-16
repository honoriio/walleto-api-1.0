from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from fastapi.responses import HTMLResponse

from src.models.usuario import Usuario
from src.services.auth_service import get_current_user
from src.core.session import create_session

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
        # ❌ REMOVIDO: validação manual do header
        # auth_header = request.headers.get("Authorization")
        # if not auth_header:
        #     raise HTTPException(status_code=401, detail="Não autenticado")
        # token = auth_header.replace("Bearer ", "")

        # ✔ agora só depende do auth_service

        session_id = create_session(current_user.id)
        dashboard_url = f"https://dashboard-dwgn.onrender.com/?session={session_id}"

        logger.info(
            "Inicialização de dashboard solicitada | usuario_id=%s",
            current_user.id
        )

        return {
            "dashboard_url": dashboard_url,
            "session": session_id
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro ao iniciar dashboard")
        raise HTTPException(status_code=500, detail="Erro interno")