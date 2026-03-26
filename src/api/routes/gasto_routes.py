from fastapi import APIRouter, HTTPException
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoListResponse
from src.services.gasto_service import criar_gasto_service, listar_gastos_service

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

