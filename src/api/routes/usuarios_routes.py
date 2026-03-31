from fastapi import APIRouter, HTTPException, Response
from src.api.schemas.usuario_schema import UsuarioCreateRequest, UsuarioResponse, UsuarioUpdateRequest, UsuarioListResponse
from src.core.exceptions import FiltroInvalidoError, NotFoundError
from src.services.usuario_service import criar_usuario_service, excluir_usuario_service, consultar_usuario_service
from datetime import date


router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario_api(dados: UsuarioCreateRequest):
    try:
        usuario_criado = criar_usuario_service(dados)
        return usuario_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    

@router.get("/", response_model=UsuarioListResponse, status_code=200)
def consultar_usuarios_api(
    nome: str | None = None,
    email: str | None = None,
    data_nscimento: date | None = None,
    sexo: str | None = None
):
    try:
        return consultar_usuario_service(
            nome=nome,
            email=email,
            data_nascimento=data_nscimento,
            sexo=sexo,
        )
    
    except FiltroInvalidoError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.delete("/{id}", status_code=204)
def excluir_usuario_api(id: int):
    try:
        excluir_usuario_service(id)
        return Response(status_code=204)
    except NotFoundError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    