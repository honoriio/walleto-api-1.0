from fastapi import APIRouter, Depends, HTTPException
from src.infrastructure.dashboard.streamlit_dashboard import encerrar_dashboard, obter_status_dashboard
from src.models.usuario import Usuario
from src.services.auth_service import get_current_user
from src.services.dashboard_service import iniciar_dashboard_com_exportacao

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/iniciar")
def iniciar_dashboard_api(current_user: Usuario = Depends(get_current_user)):
    try:
        return iniciar_dashboard_com_exportacao(current_user.id)
    except FileNotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao iniciar dashboard")


@router.post("/encerrar")
def encerrar_dashboard_api(current_user: Usuario = Depends(get_current_user)):
    try:
        return encerrar_dashboard(current_user.id)
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro ao encerrar dashboard: {erro}")


@router.get("/status")
def status_dashboard_api(current_user: Usuario = Depends(get_current_user)):
    return obter_status_dashboard(current_user.id)

