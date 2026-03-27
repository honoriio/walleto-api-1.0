from fastapi import APIRouter, HTTPException
from src.services.relatorio_service import exportar_gastos_xlsx_service


router = APIRouter(prefix="/relatorio", tags=["Relatorio"])


@router.get("/exportar/xlsx", status_code=200)
def exportar_gastos_xlsx_api():
    try:
        exportar_gastos_xlsx_service()
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    
