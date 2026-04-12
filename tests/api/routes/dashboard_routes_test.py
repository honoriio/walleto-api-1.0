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

def test_iniciar_dashboard_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_com_exportacao",
        return_value={"status": "iniciado"}
    )

    response = client.post("/dashboard/iniciar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {"status": "iniciado"}

    mock_service.assert_called_once_with(1)


def test_iniciar_dashboard_api_deve_retornar_404_quando_file_not_found(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_com_exportacao",
        side_effect=FileNotFoundError("Arquivo não encontrado")
    )

    response = client.post("/dashboard/iniciar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Arquivo não encontrado"}

    mock_service.assert_called_once_with(1)


def test_iniciar_dashboard_api_deve_retornar_400_quando_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_com_exportacao",
        side_effect=ValueError("Sem dados para exportar")
    )

    response = client.post("/dashboard/iniciar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Sem dados para exportar"}

    mock_service.assert_called_once_with(1)


def test_iniciar_dashboard_api_deve_retornar_500_quando_runtime_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_com_exportacao",
        side_effect=RuntimeError("Erro interno")
    )

    response = client.post("/dashboard/iniciar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Erro interno"}

    mock_service.assert_called_once_with(1)


def test_iniciar_dashboard_api_deve_retornar_500_quando_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mock_service = mocker.patch(
        "src.api.routes.dashboard_routes.iniciar_dashboard_com_exportacao",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/dashboard/iniciar")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno ao iniciar dashboard."
    }

    mock_service.assert_called_once_with(1)


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