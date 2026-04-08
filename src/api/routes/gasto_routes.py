import logging
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import Request
from src.core.rate_limiter import limiter
from src.api.schemas.gasto_schema import (
    GastoCreateRequest,
    GastoListResponse,
    GastoResponse,
    GastoUpdateRequest,
)
from src.core.exceptions import FiltroInvalidoError, NotFoundError
from src.models.usuario import Usuario
from src.services.auth_service import get_current_user
from src.services.gasto_service import (
    consultar_gastos_por_id_service,
    consultar_gastos_service,
    criar_gastos_service,
    editar_gastos_service,
    excluir_gastos_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoResponse, status_code=201)
@limiter.limit("10/minute")
def criar_gastos_api(request: Request, dados: GastoCreateRequest, current_user: Usuario = Depends(get_current_user),):
    logger.info("Criação de gasto iniciada | usuario_id=%s", current_user.id,)

    try:
        gasto_usuario = criar_gastos_service(dados, current_user.id)

        logger.info(
            "Gasto criado com sucesso | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_usuario.id,
        )
        return gasto_usuario

    except ValueError as erro:
        logger.warning(
            "Falha na criação de gasto por validação | usuario_id=%s | erro=%s",
            current_user.id,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception(
            "Erro inesperado ao criar gasto | usuario_id=%s",
            current_user.id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.get("/", response_model=GastoListResponse, status_code=200)
@limiter.limit("30/minute")
def consultar_gastos_api(
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
    logger.info(
        "Busca de gastos iniciada | usuario_id=%s",
        current_user.id,
    )

    try:
        gastos = consultar_gastos_service(
            usuario_id=current_user.id,
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=descricao,
            data_inicio=data_inicio,
            data_final=data_final,
        )

        logger.info(
            "Busca de gastos finalizada com sucesso | usuario_id=%s",
            current_user.id,
        )
        return gastos

    except FiltroInvalidoError as erro:
        logger.warning(
            "Falha na consulta de gastos por filtro inválido | usuario_id=%s | nome=%s | categoria=%s | valor_min=%s | valor_max=%s | data_inicio=%s | data_final=%s | erro=%s",
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
        logger.warning(
            "Falha na consulta de gastos por validação | usuario_id=%s | nome=%s | categoria=%s | valor_min=%s | valor_max=%s | erro=%s",
            current_user.id,
            nome,
            categoria,
            valor_min,
            valor_max,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception(
            "Erro inesperado ao buscar gastos | usuario_id=%s",
            current_user.id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.get("/{gasto_id}", response_model=GastoResponse, status_code=200)
@limiter.limit("30/minute")
def buscar_gasto_por_id_api(
    request: Request,
    gasto_id: int,
    current_user: Usuario = Depends(get_current_user),
):
    logger.info(
        "Busca de gasto por id iniciada | usuario_id=%s | gasto_id=%s",
        current_user.id,
        gasto_id,
    )

    try:
        gasto = consultar_gastos_por_id_service(gasto_id, current_user.id)

        logger.info(
            "Busca de gasto por id finalizada com sucesso | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_id,
        )
        return gasto

    except PermissionError as erro:
        logger.warning(
            "Acesso negado | usuario_id=%s | recurso=gasto | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=403, detail=str(erro))

    except NotFoundError as erro:
        logger.warning(
            "Gasto não encontrado | usuario_id=%s | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=404, detail=str(erro))

    except Exception:
        logger.exception(
            "Erro inesperado ao buscar gasto por id | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.patch("/{gasto_id}", response_model=GastoResponse, status_code=200)
@limiter.limit("10/minute")
def editar_gastos_api(
    request: Request,
    gasto_id: int,
    dados: GastoUpdateRequest,
    current_user: Usuario = Depends(get_current_user),
):
    logger.info(
        "Edição de gasto iniciada | usuario_id=%s | gasto_id=%s",
        current_user.id,
        gasto_id,
    )

    try:
        gasto_editado = editar_gastos_service(gasto_id, dados, current_user.id)

        logger.info(
            "Gasto editado com sucesso | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_editado.id,
        )
        return gasto_editado

    except NotFoundError as erro:
        logger.warning(
            "Gasto não encontrado para edição | usuario_id=%s | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=404, detail=str(erro))

    except ValueError as erro:
        logger.warning(
            "Falha ao editar gasto por validação | usuario_id=%s | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception(
            "Erro inesperado ao editar gasto | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.delete("/{gasto_id}", status_code=204)
@limiter.limit("5/minute")
def excluir_gastos_api(
    request: Request,
    gasto_id: int,
    current_user: Usuario = Depends(get_current_user),
):
    logger.info(
        "Exclusão de gasto iniciada | usuario_id=%s | gasto_id=%s",
        current_user.id,
        gasto_id,
    )

    try:
        excluir_gastos_service(gasto_id, current_user.id)

        logger.info(
            "Gasto excluído com sucesso | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_id,
        )
        return Response(status_code=204)

    except NotFoundError as erro:
        logger.warning(
            "Gasto não encontrado para exclusão | usuario_id=%s | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=404, detail=str(erro))

    except ValueError as erro:
        logger.warning(
            "Falha na exclusão de gasto por validação | usuario_id=%s | gasto_id=%s | erro=%s",
            current_user.id,
            gasto_id,
            erro,
        )
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception(
            "Erro inesperado ao excluir gasto | usuario_id=%s | gasto_id=%s",
            current_user.id,
            gasto_id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    