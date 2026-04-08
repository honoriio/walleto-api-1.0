import logging
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from src.core.exceptions import FiltroInvalidoError
from src.models.usuario import Usuario
from fastapi import Request
from src.core.rate_limiter import limiter
from src.services.auth_service import get_current_user
from src.services.relatorio_service import (
    exportar_gastos_pdf_services,
    exportar_gastos_xlsx_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/relatorios", tags=["Relatorios"])


@router.get("/exportar/xlsx", status_code=200)
@limiter.limit("15/hour")
def exportar_gastos_xlsx_api(
    request: Request,
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
    current_user: Usuario = Depends(get_current_user),
):
    logger.info("Exportação de gastos em xlsx iniciada | usuario_id=%s", current_user.id)

    try:
        resultado = exportar_gastos_xlsx_service(
            usuario_id=current_user.id,
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=descricao,
            data_inicio=data_inicio,
            data_final=data_final,
        )

        logger.info("Exportação de gastos em xlsx concluída com sucesso | usuario_id=%s", current_user.id)
        return resultado

    except FiltroInvalidoError as erro:
        logger.warning(
            "Falha na exportação de gastos em xlsx por filtro inválido | usuario_id=%s | nome=%s | categoria=%s | valor_min=%s | valor_max=%s | data_inicio=%s | data_final=%s | erro=%s",
            current_user.id,
            nome,
            categoria,
            valor_min,
            valor_max,
            data_inicio,
            data_final,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except ValueError as erro:
        logger.warning("Falha na exportação de gastos em xlsx por validação | usuario_id=%s | erro=%s", current_user.id, erro)
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception("Erro inesperado ao exportar gastos em xlsx | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.get("/exportar/pdf", status_code=200)
@limiter.limit("15/hour")
def exportar_gastos_pdf_api(
    request: Request,
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
    current_user: Usuario = Depends(get_current_user),
):
    logger.info("Exportação de gastos em pdf iniciada | usuario_id=%s", current_user.id)

    try:
        resultado = exportar_gastos_pdf_services(
            usuario_id=current_user.id,
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=descricao,
            data_inicio=data_inicio,
            data_final=data_final,
        )

        logger.info("Exportação de gastos em pdf concluída com sucesso | usuario_id=%s", current_user.id)
        return resultado

    except FiltroInvalidoError as erro:
        logger.warning(
            "Falha na exportação de gastos em pdf por filtro inválido | usuario_id=%s | nome=%s | categoria=%s | valor_min=%s | valor_max=%s | data_inicio=%s | data_final=%s | erro=%s",
            current_user.id,
            nome,
            categoria,
            valor_min,
            valor_max,
            data_inicio,
            data_final,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except ValueError as erro:
        logger.warning("Falha na exportação de gastos em pdf por validação | usuario_id=%s | erro=%s", current_user.id, erro)
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception("Erro inesperado ao exportar gastos em pdf | usuario_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    