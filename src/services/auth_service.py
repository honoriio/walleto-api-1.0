from passlib.context import CryptContext
from src.api.schemas.auth_schema import AuthLoginRequest
from src.repositories.usuario_repository import consultar_usuario_por_email_repository


password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def gerar_hash_senha(senha: str) -> str:
    return password_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_context.verify(senha, senha_hash)


def login_service(dados_login: AuthLoginRequest):
    usuario_auth = consultar_usuario_por_email_repository(dados_login.email)

    if not usuario_auth:
        raise ValueError("Não existe usuario com este email.")
    
    senha_valida = verificar_senha(
        dados_login.senha,
        usuario_auth.senha_hash,
    )

    if not senha_valida:
        raise ValueError("Email ou senha inválidos.")
    
    return {
        "mensagem": "Login realizado com sucesso.",
        "usuario_id": usuario_auth.id,
        "email": usuario_auth.email,
    }
