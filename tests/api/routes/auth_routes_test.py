import pytest
from fastapi import HTTPException
from starlette import status as http_status

from src.api.main import app
from src.api.routes.auth_routes import get_current_user as get_current_user_dependency


class DummyUser:
    def __init__(
        self,
        id=1,
        nome="Diego",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.sexo = sexo


# =========================================================
# TESTES - POST /auth/
# =========================================================

def test_login_usuario_api_deve_retornar_200_quando_login_for_valido(client, mocker):
    payload = {
        "email": "diego@gmail.com",
        "senha": "Senha123"
    }

    mock_login_service = mocker.patch(
        "src.api.routes.auth_routes.login_service",
        return_value={
            "access_token": "access_token_fake",
            "refresh_token": "refresh_token_fake",
            "token_type": "bearer"
        }
    )

    response = client.post("/auth/", json=payload)

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "access_token": "access_token_fake",
        "refresh_token": "refresh_token_fake",
        "token_type": "bearer"
    }
    mock_login_service.assert_called_once()


def test_login_usuario_api_deve_retornar_401_quando_service_lancar_value_error(client, mocker):
    payload = {
        "email": "diego@gmail.com",
        "senha": "SenhaErrada"
    }

    mock_login_service = mocker.patch(
        "src.api.routes.auth_routes.login_service",
        side_effect=ValueError("Email ou senha inválidos.")
    )

    response = client.post("/auth/", json=payload)

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Email ou senha inválidos."
    }
    mock_login_service.assert_called_once()


def test_login_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    payload = {
        "email": "diego@gmail.com",
        "senha": "Senha123"
    }

    mock_login_service = mocker.patch(
        "src.api.routes.auth_routes.login_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/auth/", json=payload)

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_login_service.assert_called_once()


# =========================================================
# TESTES - GET /auth/me
# =========================================================

def test_buscar_usuario_logado_api_deve_retornar_200_quando_usuario_estiver_autenticado(client):
    def override_get_current_user():
        return DummyUser(
            id=1,
            nome="Diego",
            email="diego@gmail.com",
            data_nascimento="1997-05-21",
            sexo="Masculino",
        )

    app.dependency_overrides[get_current_user_dependency] = override_get_current_user

    response = client.get("/auth/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK

    body = response.json()
    assert body["id"] == 1
    assert body["nome"] == "Diego"
    assert body["email"] == "diego@gmail.com"
    assert body["data_nascimento"] == "1997-05-21"
    assert body["sexo"] == "Masculino"


def test_buscar_usuario_logado_api_deve_retornar_401_quando_dependencia_lancar_httpexception(client):
    def override_get_current_user():
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )

    app.dependency_overrides[get_current_user_dependency] = override_get_current_user

    response = client.get("/auth/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Token inválido."
    }


# =========================================================
# TESTES - POST /auth/refresh
# =========================================================

def test_refresh_token_api_deve_retornar_200_quando_refresh_for_valido(client, mocker):
    payload = {
        "refresh_token": "refresh_token_valido"
    }

    mock_refresh_service = mocker.patch(
        "src.api.routes.auth_routes.refresh_token_service",
        return_value={
            "access_token": "novo_access_token",
            "token_type": "bearer"
        }
    )

    response = client.post("/auth/refresh", json=payload)

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "access_token": "novo_access_token",
        "token_type": "bearer"
    }

    mock_refresh_service.assert_called_once()
    args, _ = mock_refresh_service.call_args

    assert args[0] == "refresh_token_valido"
    assert isinstance(args[1], str)


def test_refresh_token_api_deve_retornar_401_quando_service_lancar_value_error(client, mocker):
    payload = {
        "refresh_token": "refresh_token_invalido"
    }

    mock_refresh_service = mocker.patch(
        "src.api.routes.auth_routes.refresh_token_service",
        side_effect=ValueError("Refresh token inválido.")
    )

    response = client.post("/auth/refresh", json=payload)

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Refresh token inválido."
    }
    mock_refresh_service.assert_called_once()


def test_refresh_token_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    payload = {
        "refresh_token": "refresh_token_valido"
    }

    mock_refresh_service = mocker.patch(
        "src.api.routes.auth_routes.refresh_token_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/auth/refresh", json=payload)

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_refresh_service.assert_called_once()