import logging
import sqlite3
from src.core.exceptions import ConflictError, NotFoundError
from src.models.usuario import Usuario
from src.services.auth_service import gerar_hash_senha
from src.api.schemas.usuario_schema import UsuarioUpdateRequest
from src.validators.usuario_validator import validar_nome_usuario, validar_email_usuario, validar_data_nascimento_usuario, validar_sexo_usuario, validar_senha_usuario, validar_id_usuario
from src.repositories.usuario_repository import consultar_usuario_por_email_repository, excluir_usuario_repository, inserir_usuario_repository, desativar_usuario_repository, consultar_usuario_por_id_repository, editar_usuario_repository

logger = logging.getLogger(__name__)


def criar_usuario_service(dados) -> Usuario:
    nome = validar_nome_usuario(dados.nome)
    email = validar_email_usuario(dados.email)
    data_nascimento = validar_data_nascimento_usuario(dados.data_nascimento)
    sexo = validar_sexo_usuario(dados.sexo)
    senha_validada = validar_senha_usuario(dados.senha)
    senha_hash = gerar_hash_senha(senha_validada)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        data_nascimento=data_nascimento,
        sexo=sexo,
        senha_hash=senha_hash,
    )

    try:
        usuario_criado = inserir_usuario_repository(novo_usuario)

        logger.info("POST /usuarios - usuário criado - usuario_id=%s email=%s", usuario_criado.id, usuario_criado.email)

        return usuario_criado

    except sqlite3.IntegrityError:
        logger.warning("Falha ao criar usuário - email já cadastrado - email=%s",email)
        raise ValueError("Email já cadastrado.")

    except Exception:
        logger.exception("Erro inesperado ao criar usuário - email=%s",email)
        raise

    
def consultar_usuario_por_id_service(id):
    usuario = consultar_usuario_por_id_repository(id)
    if not usuario:
        raise ValueError("Não existe usuario com esse ID")
    
    return usuario


def desativar_usuario_service(id: int) -> None: # Preciso fazer alterações nas nomeclaturas
    usuario_id = validar_id_usuario(id) 

    atualizado = desativar_usuario_repository(usuario_id)

    if not atualizado:
        logger.warning(f"Tentativa de desativar usuário inexistente - usuario_id: {usuario_id}")
        raise NotFoundError("Usuário não encontrado.")
    
    logger.info(f"Usuário desativado com sucesso - usuario_id: {usuario_id}")


def excluir_usuario_service(usuario_id: int) -> None:  # Preciso fazer a implementação desta função /// Preciso fazer a implementação disto aqui tambem. 
    usuario_id = validar_id_usuario(usuario_id)

    try:
        excluido = excluir_usuario_repository(usuario_id)

        if not excluido:
            logger.warning(f"Tentativa de excluir usuário inexistente - usuario_id: {usuario_id}")
            raise NotFoundError("Usuário não encontrado.")

        logger.info(f"Usuário excluído com sucesso - usuario_id: {usuario_id}")

    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de excluir usuário com dependências (gastos vinculados) - usuario_id: {usuario_id}")
        raise ValueError("Não é possível excluir usuário com gastos vinculados.")

    except Exception:
        logger.exception(f"Erro inesperado ao excluir usuário - usuario_id: {usuario_id}")
        raise
    

def editar_usuario_service(id: int, dados: UsuarioUpdateRequest) -> Usuario:
    id = validar_id_usuario(id)
    usuario_atual = consultar_usuario_por_id_repository(id)

    if not usuario_atual:
        raise NotFoundError("Não existe usuário com esse id.")

    nome_final = (
        validar_nome_usuario(dados.nome)
        if dados.nome is not None
        else usuario_atual.nome
    )

    if dados.email is not None:
        email_validado = validar_email_usuario(dados.email)
        usuario_com_mesmo_email = consultar_usuario_por_email_repository(email_validado)

        if usuario_com_mesmo_email and usuario_com_mesmo_email.id != id:
            raise ConflictError("Já existe um usuário com esse email.")

        email_final = email_validado
    else:
        email_final = usuario_atual.email

    data_nascimento_final = (
        validar_data_nascimento_usuario(dados.data_nascimento)
        if dados.data_nascimento is not None
        else usuario_atual.data_nascimento
    )

    sexo_final = (
        validar_sexo_usuario(dados.sexo)
        if dados.sexo is not None
        else usuario_atual.sexo
    )

    usuario_editado = Usuario(
        id=id,
        nome=nome_final,
        email=email_final,
        data_nascimento=data_nascimento_final,
        sexo=sexo_final,
    )

    return editar_usuario_repository(usuario_editado)
