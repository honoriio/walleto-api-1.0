import pytest
from fastapi import status
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
# FIXTURE BASE
# =========================================================
@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


# =========================================================
# /dashboard/iniciar - SUCESSO (REDIRECT)
# =========================================================
def test_iniciar_dashboard_redirect(client, monkeypatch):
    app.dependency_overrides[get_current_user] = override_user

    monkeypatch.setenv("DASHBOARD_URL", "https://dashboard.test.com")

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"},
        follow_redirects=False
    )

    assert response.status_code == 303
    assert response.headers["location"].startswith("https://dashboard.test.com/")
    assert "token=token123" in response.headers["location"]


# =========================================================
# /dashboard/iniciar - SEM AUTH HEADER
# =========================================================
def test_iniciar_dashboard_sem_token(client, monkeypatch):
    app.dependency_overrides[get_current_user] = override_user

    monkeypatch.setenv("DASHBOARD_URL", "https://dashboard.test.com")

    response = client.post("/dashboard/iniciar")

    assert response.status_code == 401
    assert response.json() == {"detail": "Não autenticado"}


# =========================================================
# /dashboard/iniciar - DASHBOARD_URL NÃO CONFIGURADA
# =========================================================
def test_iniciar_dashboard_sem_env(client, monkeypatch):
    app.dependency_overrides[get_current_user] = override_user

    monkeypatch.delenv("DASHBOARD_URL", raising=False)

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "DASHBOARD_URL não configurada"}


# =========================================================
# /dashboard/encerrar - SUCESSO
# =========================================================
def test_encerrar_dashboard(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mocker.patch(
        "src.api.routes.dashboard_routes.encerrar_dashboard",
        return_value={"status": "encerrado"}
    )

    response = client.post("/dashboard/encerrar")

    assert response.status_code == 200
    assert response.json() == {"status": "encerrado"}


# =========================================================
# /dashboard/status - SUCESSO
# =========================================================
def test_status_dashboard(client, mocker):
    app.dependency_overrides[get_current_user] = override_user

    mocker.patch(
        "src.api.routes.dashboard_routes.obter_status_dashboard",
        return_value={"ativo": True}
    )

    response = client.get("/dashboard/status")

    assert response.status_code == 200
    assert response.json() == {"ativo": True}


# =========================================================
# ERRO INTERNO - INICIAR
# =========================================================
def test_iniciar_dashboard_exception(client, monkeypatch, mocker):
    app.dependency_overrides[get_current_user] = override_user

    monkeypatch.setenv("DASHBOARD_URL", "https://dashboard.test.com")

    # força erro dentro da lógica da rota (não na dependência)
    mocker.patch(
        "src.api.routes.dashboard_routes.os.getenv",
        side_effect=Exception("fail")
    )

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"},
        follow_redirects=False
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno ao iniciar dashboard."