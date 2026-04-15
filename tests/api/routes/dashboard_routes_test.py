import pytest
from fastapi import HTTPException
from starlette import status as http_status

from src.api.main import app
from src.services.auth_service import get_current_user


# =========================================================
# DUMMY USER
# =========================================================

class DummyUser:
    def __init__(self, id=1):
        self.id = id


def override_user():
    return DummyUser(id=1)


# =========================================================
# TESTES - POST /dashboard/iniciar
# =========================================================

# mock user válido
def override_user():
    class User:
        id = 1
    return User()


# =========================================================
# SUCESSO - deve redirecionar com token
# =========================================================
def test_iniciar_dashboard_api_deve_redirecionar_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    token = "token123"

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code in (302, 307)
    assert "dashboard-dwgn.onrender.com" in response.headers["location"]
    assert "token=token123" in response.headers["location"]


# =========================================================
# ERRO 401 - sem Authorization
# =========================================================
def test_iniciar_dashboard_api_deve_retornar_401_sem_authorization(client):
    app.dependency_overrides[get_current_user] = override_user

    response = client.post(
        "/dashboard/iniciar",
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Não autenticado"}


# =========================================================
# ERRO 500 - exceção inesperada no endpoint
# =========================================================
def test_iniciar_dashboard_api_deve_retornar_500_quando_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    # mock correto: request.headers.get (não Headers.get)
    mocker.patch(
        "starlette.requests.Request.headers",
        new_callable=mocker.PropertyMock,
        return_value={}
    )

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"},
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Erro interno ao iniciar dashboard."
    }


# =========================================================
# TESTES - POST /dashboard/encerrar
# =========================================================

def test_encerrar_dashboard_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.encerrar_dashboard",
        return_value={"status": "encerrado"}
    )

    response = client.post("/dashboard/encerrar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {"status": "encerrado"}

    mock_service.assert_called_once_with(1)


def test_encerrar_dashboard_api_deve_retornar_500_quando_erro(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.encerrar_dashboard",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/dashboard/encerrar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno ao encerrar dashboard."
    }

    mock_service.assert_called_once_with(1)


# =========================================================
# TESTES - GET /dashboard/status
# =========================================================

def test_status_dashboard_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.obter_status_dashboard",
        return_value={"status": "rodando"}
    )

    response = client.get("/dashboard/status")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {"status": "rodando"}

    mock_service.assert_called_once_with(1)


def test_status_dashboard_api_deve_retornar_500_quando_erro(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.obter_status_dashboard",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/dashboard/status")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro ao obter status do dashboard."
    }

    mock_service.assert_called_once_with(1)