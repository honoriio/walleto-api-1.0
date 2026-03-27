from fastapi import APIRouter, HTTPException, Response
from decimal import Decimal
from src.core.exceptions import NotFoundError, FiltroInvalidoError
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoListResponse, GastoResponse, GastoUpdateRequest
from src.services.gasto_service import criar_gastos_service, editar_gastos_service, excluir_gastos_service, consultar_gastos_service, consultar_gastos_por_id_service

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoCreateRequest, status_code=201)
def criar_gastos_api(dados: GastoCreateRequest):
    try:
        gasto_criado = criar_gastos_service(dados)
        return gasto_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    

@router.get("/", response_model=GastoListResponse, status_code=200)
def consultar_gasto_api(
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
):
    try:
        return consultar_gastos_service(
            nome=nome,
            categoria=categoria,
            valor_min=valor_min,
            valor_max=valor_max,
            data_inicio=data_inicio,
            data_final=data_final,
        )
    except FiltroInvalidoError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")



@router.get("/{id}",response_model=GastoResponse,status_code=200)
def buscar_gastos_id_api(id: int):
    try:
        return consultar_gastos_por_id_service(id)
    
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.patch("/{id}", response_model=GastoResponse, status_code=200)
def editar_gastos_api(id: int, dados: GastoUpdateRequest):
    try:
        return editar_gastos_service(id, dados)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))   


@router.delete("/{id}", status_code=204)
def excluir_gastos_api(id: int):
    try:
        excluir_gastos_service(id)
        return Response(status_code=204)
    except NotFoundError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    