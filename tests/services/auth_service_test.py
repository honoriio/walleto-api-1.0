from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException
from starlette import status as http_status
from jose import ExpiredSignatureError, JWTError
import pytest

from src.api.schemas.auth_schema import AuthLoginRequest
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.usuario import Usuario
from src.services.auth_service import criar_access_token, criar_refresh_token, gerar_hash_senha, get_current_user, login_service, refresh_token_service, verificar_senha


#=======================================================================
#=============== Teste criação de sennha hash===========================
#=======================================================================


#Teste de senha hash com sucesso
def test_gerar_hash_senha_sucesso(mocker):
    senha = "SenhaForte123"
    hash_mock = "hash_fake"

    mock_hash = mocker.patch(
        "src.services.auth_service.password_context.hash",
        return_value=hash_mock
    )

    resultado = gerar_hash_senha(senha)

    mock_hash.assert_called_once_with(senha)
    assert resultado == hash_mock


# Teste de geração de senha hash 
@pytest.mark.parametrize(
    "senha, mensagem_esperada",
    [
        (None, "Senha inválida."),
        ("", "Senha inválida."),
        (123456, "Senha inválida."),
    ]
)
def test_gerar_hash_senha_invalida(senha, mensagem_esperada):
    with pytest.raises(ValueError) as exc:
        gerar_hash_senha(senha)

    assert str(exc.value) == mensagem_esperada


#=======================================================================
#=============== Teste de verificação de senha========================== 
#=======================================================================


# Teste de senha sucessfull
def test_verificar_senha_sucesso(mocker):
    mock_verify = mocker.patch(
        "src.services.auth_service.password_context.verify",
        return_value=True
    )

    resultado = verificar_senha("Senha123", "hash_fake")

    mock_verify.assert_called_once_with("Senha123", "hash_fake")
    assert resultado is True


# Teste de senha incorreta
def test_verificar_senha_incorreta(mocker):
    mocker.patch(
        "src.services.auth_service.password_context.verify",
        return_value=False
    )

    resultado = verificar_senha("SenhaErrada", "hash_fake")

    assert resultado is False


# Teste de senha incorreta parametrizada 
@pytest.mark.parametrize(
    "senha, senha_hash, mensagem",
    [
        (None, "hash", "Senha inválida."),
        ("", "hash", "Senha inválida."),
        ("senha", None, "Hash de senha inválido."),
        ("senha", "", "Hash de senha inválido."),
    ]
)
def test_verificar_senha_entradas_invalidas(senha, senha_hash, mensagem):
    with pytest.raises(ValueError) as exc:
        verificar_senha(senha, senha_hash)

    assert str(exc.value) == mensagem


# Teste de senha com falha interna.
def test_verificar_senha_erro_interno(mocker):
    mocker.patch(
        "src.services.auth_service.password_context.verify",
        side_effect=Exception("erro interno")
    )

    resultado = verificar_senha("senha", "hash")

    assert resultado is False


#=======================================================================
#================= Teste de login do usuario ===========================
#=======================================================================


# Teste de logi com sucesso
def test_login_service_sucesso(mocker):
    dados = AuthLoginRequest(
        email="diego@gmail.com",
        senha="Senha123"
    )

    usuario_mock = Usuario(
        id=1,
        nome="Diego",
        email="diego@gmail.com",
        senha_hash="hash_fake",
        data_nascimento=date(1997, 5, 21),
        sexo="Masculino"
    )

    mock_consultar = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_email_repository",
        return_value=usuario_mock
    )

    mock_verificar = mocker.patch(
        "src.services.auth_service.verificar_senha",
        return_value=True
    )

    mock_access = mocker.patch(
        "src.services.auth_service.criar_access_token",
        return_value="access_token_fake"
    )

    mock_refresh = mocker.patch(
        "src.services.auth_service.criar_refresh_token",
        return_value="refresh_token_fake"
    )

    resultado = login_service(dados)

    mock_consultar.assert_called_once_with(dados.email)
    mock_verificar.assert_called_once_with(dados.senha, usuario_mock.senha_hash)
    mock_access.assert_called_once()
    mock_refresh.assert_called_once_with(usuario_mock.id)

    assert resultado == {
        "access_token": "access_token_fake",
        "refresh_token": "refresh_token_fake",
        "token_type": "bearer"
    }


# Teste de login com usuario invalido. 
def test_login_service_usuario_nao_encontrado(mocker):
    dados = AuthLoginRequest(
        email="diego@gmail.com",
        senha="Senha123"
    )

    mock_consultar = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_email_repository",
        return_value=None
    )

    with pytest.raises(ValueError) as exc:
        login_service(dados)

    assert str(exc.value) == "Não existe usuario com este email."

    mock_consultar.assert_called_once_with(dados.email)


# Teste de login service senha invalida
def test_login_service_senha_invalida(mocker):
    dados = AuthLoginRequest(
        email="diego@gmail.com",
        senha="SenhaErrada"
    )

    usuario_mock = Usuario(
        id=1,
        nome="Diego",
        email="diego@gmail.com",
        senha_hash="hash_fake",
        data_nascimento=date(1997, 5, 21),
        sexo="Masculino"
    )

    mock_consultar = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_email_repository",
        return_value=usuario_mock
    )

    mock_verificar = mocker.patch(
        "src.services.auth_service.verificar_senha",
        return_value=False
    )

    with pytest.raises(ValueError) as exc:
        login_service(dados)

    assert str(exc.value) == "Email ou senha inválidos."

    mock_consultar.assert_called_once_with(dados.email)
    mock_verificar.assert_called_once_with(dados.senha, usuario_mock.senha_hash)


#=======================================================================
#=================== Teste criar acess token ===========================
#=======================================================================


# Teste criar acess token sucesso 
def test_criar_access_token_sucesso(mocker):
    dados = {
        "sub": "1",
        "email": "diego@gmail.com",
        "type": "access"
    }

    token_fake = "token_fake"

    mock_encode = mocker.patch(
        "src.services.auth_service.jwt.encode",
        return_value=token_fake
    )

    resultado = criar_access_token(dados)

    assert resultado == token_fake

    assert mock_encode.call_count == 1

    args, kwargs = mock_encode.call_args
    payload_enviado = args[0]


    assert payload_enviado["sub"] == "1"
    assert payload_enviado["email"] == "diego@gmail.com"
    assert payload_enviado["type"] == "access"
    assert "exp" in payload_enviado


# Teste de criação de acess token, mantendo o dicionario original
def test_criar_access_token_nao_altera_dict_original(mocker):
    dados = {
        "sub": "1",
        "email": "diego@gmail.com",
        "type": "access"
    }

    dados_original = dados.copy()

    mocker.patch(
        "src.services.auth_service.jwt.encode",
        return_value="token_fake"
    )

    criar_access_token(dados)

    assert dados == dados_original
    assert "exp" not in dados


# Teste de expiração de token correta 
def test_criar_access_token_expiracao_correta(mocker):
    dados = {
        "sub": "1",
        "email": "diego@gmail.com",
        "type": "access"
    }

    agora_fixo = datetime(2026, 4, 11, 10, 0, 0, tzinfo=timezone.utc)

    mock_datetime = mocker.patch(
        "src.services.auth_service.datetime"
    )

    mock_datetime.now.return_value = agora_fixo

    mock_encode = mocker.patch(
        "src.services.auth_service.jwt.encode",
        return_value="token_fake"
    )

    criar_access_token(dados)

    args, _ = mock_encode.call_args
    payload = args[0]

    exp_esperado = agora_fixo + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    assert payload["exp"] == exp_esperado


# Teste de possivel entrada invalida
@pytest.mark.parametrize(
    "entrada",
    [
        None,
        "string",
        123,
        [],
    ]
)
def test_criar_access_token_entrada_invalida(entrada):
    with pytest.raises(AttributeError):
        criar_access_token(entrada)


# =========================================================
# TESTES - get_current_user
# =========================================================

class DummyUsuario:
    def __init__(self, id=1, nome="Diego"):
        self.id = id
        self.nome = nome


def test_get_current_user_deve_retornar_usuario_quando_token_for_valido(mocker):
    token = "token_valido"
    usuario_mock = DummyUsuario(id=1, nome="Diego")

    mock_decode = mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "access"}
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository",
        return_value=usuario_mock
    )

    resultado = get_current_user(token)

    assert resultado == usuario_mock
    mock_decode.assert_called_once_with(
        token,
        mocker.ANY,
        algorithms=[mocker.ANY]
    )
    mock_consultar_usuario.assert_called_once_with(1)


def test_get_current_user_deve_lancar_401_quando_sub_estiver_ausente(mocker):
    token = "token_sem_sub"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"type": "access"}
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."
    mock_consultar_usuario.assert_not_called()


def test_get_current_user_deve_lancar_401_quando_type_nao_for_access(mocker):
    token = "token_tipo_invalido"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "refresh"}
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."
    mock_consultar_usuario.assert_not_called()


def test_get_current_user_deve_lancar_401_quando_usuario_nao_for_encontrado(mocker):
    token = "token_usuario_inexistente"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "access"}
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository",
        return_value=None
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."
    mock_consultar_usuario.assert_called_once_with(1)


def test_get_current_user_deve_lancar_401_quando_jwt_for_invalido(mocker):
    token = "token_invalido"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        side_effect=JWTError()
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."
    mock_consultar_usuario.assert_not_called()


def test_get_current_user_deve_lancar_401_quando_sub_nao_for_inteiro_valido(mocker):
    token = "token_sub_invalido"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "abc", "type": "access"}
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."
    mock_consultar_usuario.assert_not_called()


def test_get_current_user_deve_relancar_httpexception_sem_converter_para_500(mocker):
    token = "token_com_httpexception"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "access"}
    )
    mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository",
        side_effect=HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."


def test_get_current_user_deve_lancar_500_em_erro_inesperado(mocker):
    token = "token_erro_inesperado"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        side_effect=Exception("erro inesperado")
    )
    mock_consultar_usuario = mocker.patch(
        "src.services.auth_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)

    assert exc.value.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == "Erro interno do servidor."
    mock_consultar_usuario.assert_not_called()


# =========================================================
# TESTES - criar_refresh_token
# =========================================================

def test_criar_refresh_token_deve_gerar_token_com_payload_correto(mocker):
    usuario_id = 1
    token_esperado = "refresh_token_gerado"

    fake_now = datetime(2026, 4, 12, 12, 0, 0, tzinfo=timezone.utc)
    exp_esperado = fake_now + timedelta(days=15)

    mock_datetime = mocker.patch("src.services.auth_service.datetime")
    mock_datetime.now.return_value = fake_now

    mock_encode = mocker.patch(
        "src.services.auth_service.jwt.encode",
        return_value=token_esperado
    )

    resultado = criar_refresh_token(usuario_id)

    assert resultado == token_esperado
    mock_encode.assert_called_once()

    args, kwargs = mock_encode.call_args
    payload_enviado = args[0]

    assert payload_enviado["sub"] == "1"
    assert payload_enviado["type"] == "refresh"
    assert payload_enviado["exp"] == exp_esperado
    assert kwargs["algorithm"] == mocker.ANY


def test_criar_refresh_token_deve_converter_usuario_id_para_string_no_payload(mocker):
    usuario_id = 99

    fake_now = datetime(2026, 4, 12, 12, 0, 0, tzinfo=timezone.utc)

    mock_datetime = mocker.patch("src.services.auth_service.datetime")
    mock_datetime.now.return_value = fake_now

    mock_encode = mocker.patch(
        "src.services.auth_service.jwt.encode",
        return_value="token"
    )

    criar_refresh_token(usuario_id)

    args, _ = mock_encode.call_args
    payload_enviado = args[0]

    assert isinstance(payload_enviado["sub"], str)
    assert payload_enviado["sub"] == "99"


def test_criar_refresh_token_deve_propagar_erro_se_encode_falhar(mocker):
    usuario_id = 1

    fake_now = datetime(2026, 4, 12, 12, 0, 0, tzinfo=timezone.utc)

    mock_datetime = mocker.patch("src.services.auth_service.datetime")
    mock_datetime.now.return_value = fake_now

    mocker.patch(
        "src.services.auth_service.jwt.encode",
        side_effect=Exception("falha ao gerar token")
    )

    with pytest.raises(Exception) as exc:
        criar_refresh_token(usuario_id)

    assert str(exc.value) == "falha ao gerar token"


# =========================================================
# TESTES - refresh_token_service
# =========================================================

def test_refresh_token_service_deve_retornar_novo_access_token_quando_refresh_for_valido(mocker):
    refresh_token = "refresh_valido"
    ip = "127.0.0.1"

    mock_decode = mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "refresh"}
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token",
        return_value="novo_access_token"
    )

    resultado = refresh_token_service(refresh_token, ip)

    assert resultado == {
        "access_token": "novo_access_token",
        "token_type": "bearer"
    }

    mock_decode.assert_called_once_with(
        refresh_token,
        mocker.ANY,
        algorithms=[mocker.ANY]
    )
    mock_criar_access.assert_called_once_with(
        data={
            "sub": "1",
            "type": "access"
        }
    )


def test_refresh_token_service_deve_lancar_401_quando_type_nao_for_refresh(mocker):
    refresh_token = "token_invalido"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "access"}
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Refresh token inválido."
    mock_criar_access.assert_not_called()


def test_refresh_token_service_deve_lancar_401_quando_sub_estiver_ausente(mocker):
    refresh_token = "token_sem_sub"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"type": "refresh"}
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Refresh token inválido."
    mock_criar_access.assert_not_called()


def test_refresh_token_service_deve_lancar_401_quando_sub_nao_for_inteiro_valido(mocker):
    refresh_token = "token_sub_invalido"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "abc", "type": "refresh"}
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Refresh token inválido."
    mock_criar_access.assert_not_called()


def test_refresh_token_service_deve_lancar_401_quando_refresh_token_estiver_expirado(mocker):
    refresh_token = "token_expirado"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        side_effect=ExpiredSignatureError()
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Refresh token expirado."
    mock_criar_access.assert_not_called()


def test_refresh_token_service_deve_lancar_401_quando_jwt_for_invalido(mocker):
    refresh_token = "token_jwt_invalido"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        side_effect=JWTError()
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Refresh token inválido."
    mock_criar_access.assert_not_called()


def test_refresh_token_service_deve_relancar_httpexception_sem_converter_para_500(mocker):
    refresh_token = "token_com_httpexception"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        return_value={"sub": "1", "type": "refresh"}
    )
    mocker.patch(
        "src.services.auth_service.criar_access_token",
        side_effect=HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="erro http controlado"
        )
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "erro http controlado"


def test_refresh_token_service_deve_lancar_500_em_erro_inesperado(mocker):
    refresh_token = "token_erro_inesperado"
    ip = "127.0.0.1"

    mocker.patch(
        "src.services.auth_service.jwt.decode",
        side_effect=Exception("erro inesperado")
    )
    mock_criar_access = mocker.patch(
        "src.services.auth_service.criar_access_token"
    )

    with pytest.raises(HTTPException) as exc:
        refresh_token_service(refresh_token, ip)

    assert exc.value.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == "Erro interno do servidor."
    mock_criar_access.assert_not_called()