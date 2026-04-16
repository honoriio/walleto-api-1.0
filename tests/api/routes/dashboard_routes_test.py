import pytest
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

def test_iniciar_dashboard_api(client):
    app.dependency_overrides[get_current_user] = override_user

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()
    assert "dashboard_url" in data
    assert "session=" in data["dashboard_url"]


def test_iniciar_dashboard_401(client):
    # ✔ ALTERAÇÃO IMPORTANTE:
    # agora precisa forçar falha de autenticação via override vazio
    app.dependency_overrides[get_current_user] = lambda: (_ for _ in ()).throw(
        Exception("unauthorized")
    )

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED


# =========================================================
# TESTES - POST /dashboard/encerrar (PLACEHOLDER)
# =========================================================

def test_encerrar_dashboard_api_placeholder(client):
    response = client.post("/dashboard/encerrar")

    assert response.status_code in (
        http_status.HTTP_200_OK,
        http_status.HTTP_404_NOT_FOUND
    )


# =========================================================
# TESTES - GET /dashboard/status (PLACEHOLDER)
# =========================================================

def test_status_dashboard_api_placeholder(client):
    response = client.get("/dashboard/status")

    assert response.status_code in (
        http_status.HTTP_200_OK,
        http_status.HTTP_404_NOT_FOUND
    )