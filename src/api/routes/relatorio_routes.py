from fastapi import APIRouter, HTTPException
from src.services.relatorio_service import exportar_gastos_xlsx_service


router = APIRouter(prefix="/relatorios", tags=["Relatorios"])


@router.get("/exportar/xlsx", status_code=200)
def exportar_gastos_xlsx_api():
    try:
        caminho_arquivo = exportar_gastos_xlsx_service()
        return {
            "arquivo": caminho_arquivo
        }
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    
