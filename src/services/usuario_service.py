from src.core.exceptions import NotFoundError
from src.models.usuario import Usuario
from datetime import date
from passlib.context import CryptContext
from src.validators.usuario_validator import validar_nome_usuario, validar_email_usuario, validar_data_nascimento_usuario, validar_sexo_usuario, validar_senha_usuario, validar_id_usuario
from src.repositories.usuario_repository import inserir_usuario_repository, excluir_usuario_repository



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



pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)



def excluir_usuario_service(id: int) -> None:
    id = validar_id_usuario(id)


    excluido = excluir_usuario_repository(id)

    if not excluido:
        raise NotFoundError("Não existe gasto com esse ID.")