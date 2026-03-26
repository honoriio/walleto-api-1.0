from fastapi import APIRouter, HTTPException
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoListResponse, GastoResponse
from src.services.gasto_service import criar_gasto_service, listar_gastos_service, buscar_gasto_por_id_service,  buscar_gastos_por_categoria_service

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoCreateRequest, status_code=201)
def criar_gasto_api(dados: GastoCreateRequest):
    try:
        gasto_criado = criar_gasto_service(dados)
        return gasto_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    


@router.get("/", response_model=GastoListResponse, status_code=200)
def listar_gasto_api():
    return listar_gastos_service()


@router.get("/categoria", response_model=GastoListResponse, status_code=200)
def buscar_gasto_categoria_api(categoria: str):
    try:
        return buscar_gastos_por_categoria_service(categoria)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    

@router.get("/{id}",response_model=GastoResponse,status_code=200)
def buscar_gasto_id_api(id: int):
    try:
        return buscar_gasto_por_id_service(id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    
