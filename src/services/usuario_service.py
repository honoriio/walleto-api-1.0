from src.core.exceptions import ConflictError, NotFoundError
from src.models.usuario import Usuario
from src.services.auth_service import gerar_hash_senha
from src.api.schemas.usuario_schema import UsuarioUpdateRequest
from src.validators.usuario_validator import validar_nome_usuario, validar_email_usuario, validar_data_nascimento_usuario, validar_sexo_usuario, validar_senha_usuario, validar_id_usuario
from src.repositories.usuario_repository import consultar_usuario_por_email_repository, inserir_usuario_repository, excluir_usuario_repository, consultar_usuarios_repository, consultar_usuario_por_id_repository, editar_usuarios_repository



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
        senha_hash=senha_hash
    )

    usuario_criado = inserir_usuario_repository(novo_usuario)
    return usuario_criado


def consultar_usuario_service(
        nome=None,
        email=None,
        data_nascimento=None,
        sexo=None
):
    
    if nome is not None:
        nome = validar_nome_usuario(nome)

    if email is not None:
        email = validar_email_usuario(email)

    if data_nascimento is not None:
        data_nascimento = validar_data_nascimento_usuario(data_nascimento)

    if sexo is not None:
        sexo = validar_sexo_usuario(sexo)


    usuarios = consultar_usuarios_repository(
        nome=nome,
        email=email,
        data_nascimento=data_nascimento,
        sexo=sexo,
    )

    return {
        "usuarios": usuarios,
        "quantidade": len(usuarios)
    }


def consultar_usuario_por_id_service(id):
    usuario = consultar_usuario_por_id_repository(id)
    if not usuario:
        raise ValueError("Não existe usuario com esse ID")
    
    return usuario


def excluir_usuario_service(id: int) -> None:
    id = validar_id_usuario(id)


    excluido = excluir_usuario_repository(id)

    if not excluido:
        raise NotFoundError("Não existe gasto com esse ID.")
    

def editar_usuarios_service(id: int, dados: UsuarioUpdateRequest) -> Usuario:
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

    return editar_usuarios_repository(usuario_editado)
