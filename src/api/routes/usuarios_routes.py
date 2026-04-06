from fastapi import APIRouter, Depends, HTTPException, Response
from src.api.schemas.usuario_schema import UsuarioCreateRequest, UsuarioResponse, UsuarioUpdateRequest
from src.core.exceptions import ConflictError, NotFoundError
from src.models.usuario import Usuario
import logging
from src.services.auth_service import get_current_user
from src.services.usuario_service import criar_usuario_service, desativar_usuario_service, excluir_usuario_service, consultar_usuario_por_id_service, editar_usuario_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario_api(dados: UsuarioCreateRequest):
    try:
        usuario_criado = criar_usuario_service(dados)
        return usuario_criado
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        logger.exception("Erro inesperado na rota de criação de usuário")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.get("/me", response_model=UsuarioResponse, status_code=200)
def consultar_meu_usuario_api(current_user: Usuario = Depends(get_current_user)):
    try:
        return consultar_usuario_por_id_service(current_user.id)

    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.patch("/me", response_model=UsuarioResponse, status_code=200)
def editar_usuario_api(dados: UsuarioUpdateRequest, current_user: Usuario = Depends(get_current_user)):
    try:
        return editar_usuario_service(current_user.id, dados)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except ConflictError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    

@router.patch("/me/desativar", status_code=204, include_in_schema=False) #///A mesma esta desativada do painel do sweger  # Desativa o usuario o usuario logado apenas, o mesmo pode ser reativado depois, isso vai ser usado em uma feature futura
def desativar_usuario_api(current_user: Usuario = Depends(get_current_user)):# preciso melhorar os erros e adicionar logs
    try:
        desativar_usuario_service(current_user.id)
        return Response(status_code=204)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    

@router.delete("/me", status_code=204)
def excluir_usuario_api(current_user: Usuario = Depends(get_current_user)):
    try:
        excluir_usuario_service(current_user.id)
        return Response(status_code=204)
    except NotFoundError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    
