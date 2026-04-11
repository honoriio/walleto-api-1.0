from datetime import date, datetime, timedelta, timezone

import pytest

from src.api.schemas.auth_schema import AuthLoginRequest
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.usuario import Usuario
from src.services.auth_service import criar_access_token, gerar_hash_senha, login_service, verificar_senha


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


#=======================================================================
#=================== Teste de current user =============================
#=======================================================================

