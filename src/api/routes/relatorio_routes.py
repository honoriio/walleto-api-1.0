from fastapi import APIRouter, Depends, HTTPException
from src.core.exceptions import FiltroInvalidoError
from decimal import Decimal
from src.models.usuario import Usuario
from src.services.auth_service import get_current_user
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
    current_user: Usuario = Depends(get_current_user)
):
    try:
        return exportar_gastos_xlsx_service(
            usuario_id=current_user.id,
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
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    

@router.get("/exportar/pdf", status_code=200)
def exportar_gastos_pdf_api(
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
    current_user: Usuario = Depends(get_current_user)
):
    try:
        return exportar_gastos_pdf_services(
            usuario_id=current_user.id,
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
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    