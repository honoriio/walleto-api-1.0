from fastapi import APIRouter, HTTPException, Response
from src.core.exceptions import NotFoundError
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoListResponse, GastoResponse, GastoUpdateRequest
from src.services.gasto_service import criar_gastos_service, listar_gastos_service, buscar_gastos_por_id_service,  buscar_gastos_por_categoria_service,buscar_gastos_por_nome_service, buscar_gastos_por_valor_service, buscar_gastos_por_data_service, editar_gastos_service, excluir_gastos_service

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoCreateRequest, status_code=201)
def criar_gastos_api(dados: GastoCreateRequest):
    try:
        gasto_criado = criar_gastos_service(dados)
        return gasto_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    


@router.get("/", response_model=GastoListResponse, status_code=200)
def listar_gastos_api():
    return listar_gastos_service()


@router.get("/categoria", response_model=GastoListResponse, status_code=200)
def buscar_gastos_categoria_api(categoria: str):
    try:
        return buscar_gastos_por_categoria_service(categoria)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    

@router.get("/nome", response_model=GastoListResponse, status_code=200)
def buscar_gastos_por_nome_api(nome: str):
    try:
        return buscar_gastos_por_nome_service(nome)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    

@router.get("/valor", response_model=GastoListResponse, status_code=200)
def buscar_gastos_por_valor_api(
    valor_min: float | None = None,
    valor_max: float | None = None
):
    try:
        return buscar_gastos_por_valor_service(valor_min, valor_max)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    

@router.get("/data", response_model=GastoListResponse, status_code=200)
def buscar_gastos_por_data_api(
    data_inicio: str | None = None,
    data_final: str  | None = None
):
    try:
        return buscar_gastos_por_data_service(data_inicio, data_final)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/{id}",response_model=GastoResponse,status_code=200)
def buscar_gastos_id_api(id: int):
    try:
        return buscar_gastos_por_id_service(id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


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
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))