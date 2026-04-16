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

def test_iniciar_dashboard_api_deve_redirecionar_quando_sucesso(client):
    app.dependency_overrides[get_current_user] = override_user

    token = "token123"

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code == 307
    assert "token=token123" in response.headers["location"]


def test_iniciar_dashboard_api_deve_retornar_401_sem_authorization(client):
    app.dependency_overrides[get_current_user] = override_user

    response = client.post(
        "/dashboard/iniciar",
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Não autenticado"}


def test_iniciar_dashboard_api_deve_retornar_500_quando_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_api",
        side_effect=Exception("erro inesperado")
    )

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"},
        follow_redirects=False
    )

    app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro interno"}


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
    assert response.json() == {"detail": "Erro interno"}

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
    assert response.json() == {"detail": "Erro interno"}

    mock_service.assert_called_once_with(1)