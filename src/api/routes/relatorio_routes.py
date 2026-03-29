from fastapi import APIRouter, HTTPException
from src.core.exceptions import FiltroInvalidoError
from src.api.schemas.gasto_schema import GastoListResponse
from decimal import Decimal
from src.services.relatorio_service import exportar_gastos_xlsx_service, exportar_gastos_pdf_services


router = APIRouter(prefix="/relatorios", tags=["Relatorios"])

    
@router.get("/exportar/xlsx", status_code=200)
def exportar_gastos_xlsx_api(
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
):
    try:
        return exportar_gastos_xlsx_service(
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=descricao,
            data_inicio=data_inicio,
            data_final=data_final,
        )

    except FiltroInvalidoError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(erro)}")
    

@router.get("/exportar/pdf", status_code=200)
def exportar_gastos_pdf_api(
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
):
    try:
        return exportar_gastos_pdf_services(
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=descricao,
            data_inicio=data_inicio,
            data_final=data_final,
        )

    except FiltroInvalidoError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(erro)}")
    