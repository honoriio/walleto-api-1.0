from fastapi import APIRouter, Depends, HTTPException, Response
from src.api.schemas.usuario_schema import UsuarioCreateRequest, UsuarioResponse, UsuarioUpdateRequest
from src.core.exceptions import ConflictError, NotFoundError
from src.models.usuario import Usuario
import logging
from fastapi import Request
from src.core.rate_limiter import limiter
from src.services.auth_service import get_current_user
from src.services.usuario_service import criar_usuario_service, desativar_usuario_service, excluir_usuario_service, consultar_usuario_por_id_service, editar_usuario_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usuario", tags=["Usuários"])


@router.post("/", response_model=UsuarioResponse, status_code=201,     summary="Cria um novo usuário",
    description="""
Cria uma nova conta de usuário no sistema.
Retorna os dados do usuário criado.
"""
)
@limiter.limit("3/minute")
def criar_usuario_api(request: Request, dados: UsuarioCreateRequest):
    logger.info(f"Tentativa de criação de novo usuário | email={dados.email}")
    try:
        usuario_criado = criar_usuario_service(dados)
        logger.info(f"Usuário criado com sucesso | usuario_id={usuario_criado.id}")
        return usuario_criado

    except ValueError as erro:
        logger.warning(f"Falha na criação de usuário por validação | email={dados.email} | erro={erro}")
        raise HTTPException(status_code=400, detail=str(erro))

    except Exception:
        logger.exception(f"Erro inesperado ao criar usuário | email={dados.email}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


#Consulta os dados do usuario logado
@router.get("/me", response_model=UsuarioResponse, status_code=200, summary="Obtém os dados do usuário autenticado",
    description="""
Retorna as informações do usuário atualmente autenticado.
"""
)
def consultar_meu_usuario_api(current_user: Usuario = Depends(get_current_user)):
    logger.info(f"Usuário ID {current_user.id} solicitou seus próprios dados.")
    try:
        usuario = consultar_usuario_por_id_service(current_user.id)
        logger.debug(f"Dados recuperados com sucesso para o ID {current_user.id}")
        return usuario

    except NotFoundError as erro:
        logger.warning(f"Inconsistência: Usuário autenticado {current_user.id} não encontrado no banco. Erro: {erro}")
        raise HTTPException(status_code=404, detail=str(erro))
        
    except ValueError as erro:
        logger.error(f"Erro de validação para o usuário {current_user.id}: {erro}")
        raise HTTPException(status_code=400, detail=str(erro))
        
    except Exception as e:
        logger.exception(f"Erro inesperado ao consultar perfil do usuário {current_user.id}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Atualiza os dados do usuario logado, como, nome, data de nascimento, sexo e email.  em breve irei adicionar uma função de validar o email via codigo, para facilitar a troca do email e da senha
@router.patch("/me", response_model=UsuarioResponse, status_code=200, summary="Atualiza os dados do usuário",
    description="""
Atualiza as informações do usuário autenticado, como nome, email e dados pessoais.
""")
@limiter.limit("10/minute")
def editar_usuario_api(request: Request, dados: UsuarioUpdateRequest, current_user: Usuario = Depends(get_current_user)):
    campos_atualizados = dados.dict(exclude_unset=True)
    campos_atualizados.pop("senha", None)

    logger.info(f"Atualização de usuário iniciada | usuario_id={current_user.id} | campos={list(campos_atualizados.keys())}")
    try:
        usuario_atualizado = editar_usuario_service(current_user.id, dados)
        logger.info(f"Dados do usuário atualizados com sucesso | usuario_id={current_user.id}")
        return usuario_atualizado

    except NotFoundError as erro:
        logger.warning(f"Usuário não encontrado para atualização | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=404, detail=str(erro))

    except ValueError as erro:
        logger.warning(f"Falha de validação ao atualizar usuário | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=400, detail=str(erro))

    except ConflictError as erro:
        logger.warning(f"Conflito ao atualizar usuário | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=409, detail=str(erro))

    except Exception:
        logger.exception(f"Erro inesperado ao atualizar usuário | usuario_id={current_user.id}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    

# Desativa a conta do usuário autenticado (soft delete).
# Será utilizada no fluxo de exclusão com período de reativação antes da remoção definitiva.
# Observação: funcionalidade ainda não exposta como rota na API.
def desativar_usuario_api(current_user: Usuario = Depends(get_current_user)):
    logger.info(f"Desativação de conta do usuário iniciada | usuario_id={current_user.id}")
    try:
        desativar_usuario_service(current_user.id)
        logger.info(f"Conta desativada com sucesso | usuario_id={current_user.id}")
        return Response(status_code=204)

    except ValueError as erro:
        logger.warning(f"Falha de validação ao desativar conta | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=400, detail=str(erro))

    except NotFoundError as erro:
        logger.warning(f"Usuário não encontrado para desativação | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=404, detail=str(erro))

    except Exception:
        logger.exception(f"Erro inesperado ao desativar conta | usuario_id={current_user.id}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")

    

# Exclui permanentemente a conta do usuário autenticado.
# Os dados relacionados, como os gastos, também são removidos automaticamente via cascade. 
@router.delete("/me", status_code=204,     summary="Exclui a conta do usuário",
    description="""
Remove permanentemente a conta do usuário autenticado e seus dados associados.
""")
@limiter.limit("1/hour")
def excluir_usuario_api(request: Request, current_user: Usuario = Depends(get_current_user)):
    logger.info(f"Exclusão da conta do usuário iniciada | usuario_id={current_user.id}")
    try:
        excluir_usuario_service(current_user.id)
        logger.info(f"Conta do usuário excluida com sucesso | usuario_id={current_user.id}")
        return Response(status_code=204)
    
    except ValueError as erro:
        logger.warning(f"Falha de validação ao excluir conta | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=400, detail=str(erro))
    
    except NotFoundError as erro:
        logger.warning(f"Usuário não encontrado para exclusão | usuario_id={current_user.id} | erro={erro}")
        raise HTTPException(status_code=404, detail=str(erro))
    
    except Exception:
        logger.exception(f"Erro inesperado ao excluir conta | usuario_id={current_user.id}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    
