from fastapi import APIRouter, HTTPException, Response
from src.api.schemas.usuario_schema import UsuarioCreateRequest, UsuarioResponse, UsuarioUpdateRequest, UsuarioListResponse
from src.services.usuario_service import criar_usuario_service


router = APIRouter(prefix="/usuário", tags=["Usuário"])

@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario_api(dados: UsuarioCreateRequest):
    try:
        usuario_criado = criar_usuario_service(dados)
        return usuario_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))