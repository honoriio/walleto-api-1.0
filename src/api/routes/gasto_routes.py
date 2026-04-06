from fastapi import APIRouter, Depends, HTTPException, Response, logger
from decimal import Decimal
from src.core.exceptions import NotFoundError, FiltroInvalidoError
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoListResponse, GastoResponse, GastoUpdateRequest
from src.models.usuario import Usuario
from src.services.auth_service import get_current_user
from src.services.gasto_service import criar_gastos_service, editar_gastos_service, excluir_gastos_service, consultar_gastos_service, consultar_gastos_por_id_service


router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoResponse, status_code=201)
def criar_gastos_api(dados: GastoCreateRequest, current_user: Usuario = Depends(get_current_user)):
    try:
        return criar_gastos_service(dados, current_user.id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    

@router.get("/", response_model=GastoListResponse, status_code=200)
def consultar_gastos_api(
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
        return consultar_gastos_service(
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
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/{gasto_id}")
def buscar_gasto_por_id_api(gasto_id: int, usuario_logado=Depends(get_current_user)):
    try:
        return consultar_gastos_por_id_service(gasto_id, usuario_logado.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.exception(
            "Erro inesperado ao buscar gasto por id - usuario_id=%s gasto_id=%s",
            usuario_logado.id,
            gasto_id,
        )
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.patch("/{id}", response_model=GastoResponse, status_code=200)
def editar_gastos_api(id: int, dados: GastoUpdateRequest, current_user: Usuario = Depends(get_current_user)):
    try:
        return editar_gastos_service(id, dados, current_user.id)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/{id}", status_code=204)
def excluir_gastos_api(id: int, current_user: Usuario = Depends(get_current_user)):
    try:
        excluir_gastos_service(id, current_user.id)
        return Response(status_code=204)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    