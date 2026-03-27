from fastapi import APIRouter, HTTPException


from src.infrastructure.dashboard.streamlit_dashboard import (
    encerrar_dashboard,
    obter_status_dashboard,
)
from src.services.dashboard_service import iniciar_dashboard_com_exportacao

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.post("/iniciar")
def iniciar_dashboard_api():
    try:
        return iniciar_dashboard_com_exportacao()
    except FileNotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao iniciar dashboard: {erro}",
        )


@router.get("/status")
def status_dashboard_api():
    return obter_status_dashboard()


@router.post("/encerrar")
def encerrar_dashboard_api():
    try:
        return encerrar_dashboard()
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro ao encerrar dashboard: {erro}")