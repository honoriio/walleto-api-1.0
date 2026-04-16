from typing import Dict, List

import pytest
from starlette import status as http_status

from src.api.main import app
from src.services.auth_service import get_current_user
from src.services.gasto_service import consultar_gastos_service


# =========================================================
# DUMMY USER
# =========================================================

class DummyUser:
    def __init__(self, id=1):
        self.id = id


def override_user():
    return DummyUser(id=1)



def test_iniciar_dashboard_api(client):
    app.dependency_overrides[get_current_user] = override_user

    response = client.post(
        "/dashboard/iniciar",
        headers={"Authorization": "Bearer token123"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "Abrir Dashboard" in response.text
    assert "session=" in response.text


def test_iniciar_dashboard_401(client):
    response = client.post("/dashboard/iniciar")

    assert response.status_code == 401


def test_encerrar_dashboard_api_placeholder(client):
    response = client.post("/dashboard/encerrar")

    assert response.status_code in (200, 404)


def test_status_dashboard_api_placeholder(client):
    response = client.get("/dashboard/status")

    assert response.status_code in (200, 404)