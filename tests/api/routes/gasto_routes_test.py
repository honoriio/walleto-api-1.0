from datetime import date
from decimal import Decimal

from starlette import status as http_status

from src.api.main import app
from src.api.routes.gasto_routes import get_current_user
from src.core.exceptions import FiltroInvalidoError, NotFoundError


class DummyUser:
    def __init__(self, id=1):
        self.id = id


class DummyGasto:
    def __init__(
        self,
        id=1,
        nome="Mercado",
        valor="100.50",
        categoria="Alimentação",
        descricao="Compra do mês",
        data="2026-04-12",
        usuario_id=1,
    ):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.categoria = categoria
        self.descricao = descricao
        self.data = data
        self.usuario_id = usuario_id


def override_get_current_user():
    return DummyUser(id=1)


# =========================================================
# TESTES - POST /gastos/
# =========================================================

def test_criar_gastos_api_deve_retornar_201_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Mercado",
        "valor": "100.50",
        "categoria": "Alimentação",
        "descricao": "Compra do mês",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.criar_gastos_service",
        return_value=DummyGasto()
    )

    response = client.post("/gastos/", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "nome": "Mercado",
        "valor": "100.50",
        "categoria": "Alimentação",
        "descricao": "Compra do mês",
        "data": "2026-04-12",
        "usuario_id": 1,
    }
    mock_service.assert_called_once()


def test_criar_gastos_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "",
        "valor": "100.50",
        "categoria": "Alimentação",
        "descricao": "Compra do mês",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.criar_gastos_service",
        side_effect=ValueError("O nome do gasto não pode estar em branco")
    )

    response = client.post("/gastos/", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "O nome do gasto não pode estar em branco"
    }
    mock_service.assert_called_once()


def test_criar_gastos_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Mercado",
        "valor": "100.50",
        "categoria": "Alimentação",
        "descricao": "Compra do mês",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.criar_gastos_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/gastos/", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once()


# =========================================================
# TESTES - GET /gastos/
# =========================================================

def test_consultar_gastos_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    retorno_service = {
        "gastos": [
            {
                "id": 1,
                "nome": "Mercado",
                "valor": "100.50",
                "categoria": "Alimentação",
                "descricao": "Compra do mês",
                "data": "2026-04-12",
                "usuario_id": 1,
            }
        ],
        "total": Decimal("100.50"),
        "quantidade": 1,
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_service",
        return_value=retorno_service
    )

    response = client.get(
        "/gastos/",
        params={
            "nome": "Mercado",
            "categoria": "Alimentação",
            "valor_min": "10.00",
            "valor_max": "500.00",
            "descricao": "Compra",
            "data_inicio": "2026-04-01",
            "data_final": "2026-04-30",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "gastos": [
            {
                "id": 1,
                "nome": "Mercado",
                "valor": "100.50",
                "categoria": "Alimentação",
                "descricao": "Compra do mês",
                "data": "2026-04-12",
                "usuario_id": 1,
            }
        ],
        "total": "100.50",
        "quantidade": 1,
    }

    mock_service.assert_called_once_with(
        usuario_id=1,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=Decimal("10.00"),
        valor_max=Decimal("500.00"),
        descricao="Compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )


def test_consultar_gastos_api_deve_retornar_400_quando_service_lancar_filtro_invalido_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_service",
        side_effect=FiltroInvalidoError("Filtro inválido.")
    )

    response = client.get("/gastos/")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Filtro inválido."
    }
    mock_service.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )


def test_consultar_gastos_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_service",
        side_effect=ValueError("Valor mínimo inválido.")
    )

    response = client.get("/gastos/")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Valor mínimo inválido."
    }
    mock_service.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )


def test_consultar_gastos_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/gastos/")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )


# =========================================================
# TESTES - GET /gastos/{gasto_id}
# =========================================================

def test_buscar_gasto_por_id_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_por_id_service",
        return_value=DummyGasto()
    )

    response = client.get("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "nome": "Mercado",
        "valor": "100.50",
        "categoria": "Alimentação",
        "descricao": "Compra do mês",
        "data": "2026-04-12",
        "usuario_id": 1,
    }
    mock_service.assert_called_once_with(1, 1)


def test_buscar_gasto_por_id_api_deve_retornar_403_quando_service_lancar_permission_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_por_id_service",
        side_effect=PermissionError("Acesso negado.")
    )

    response = client.get("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Acesso negado."
    }
    mock_service.assert_called_once_with(1, 1)


def test_buscar_gasto_por_id_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_por_id_service",
        side_effect=NotFoundError("Gasto não encontrado.")
    )

    response = client.get("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Gasto não encontrado."
    }
    mock_service.assert_called_once_with(1, 1)


def test_buscar_gasto_por_id_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.consultar_gastos_por_id_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once_with(1, 1)


# =========================================================
# TESTES - PATCH /gastos/{gasto_id}
# =========================================================

def test_editar_gastos_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Mercado Atualizado",
        "valor": "150.75",
        "categoria": "Alimentação",
        "descricao": "Compra atualizada",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.editar_gastos_service",
        return_value=DummyGasto(
            id=1,
            nome="Mercado Atualizado",
            valor="150.75",
            categoria="Alimentação",
            descricao="Compra atualizada",
            data="2026-04-12",
            usuario_id=1,
        )
    )

    response = client.patch("/gastos/1", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "nome": "Mercado Atualizado",
        "valor": "150.75",
        "categoria": "Alimentação",
        "descricao": "Compra atualizada",
        "data": "2026-04-12",
        "usuario_id": 1,
    }
    mock_service.assert_called_once()


def test_editar_gastos_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Mercado Atualizado",
        "valor": "150.75",
        "categoria": "Alimentação",
        "descricao": "Compra atualizada",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.editar_gastos_service",
        side_effect=NotFoundError("Gasto não encontrado.")
    )

    response = client.patch("/gastos/1", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Gasto não encontrado."
    }
    mock_service.assert_called_once()


def test_editar_gastos_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "",
        "valor": "150.75",
        "categoria": "Alimentação",
        "descricao": "Compra atualizada",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.editar_gastos_service",
        side_effect=ValueError("O nome do gasto não pode estar em branco")
    )

    response = client.patch("/gastos/1", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "O nome do gasto não pode estar em branco"
    }
    mock_service.assert_called_once()


def test_editar_gastos_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Mercado Atualizado",
        "valor": "150.75",
        "categoria": "Alimentação",
        "descricao": "Compra atualizada",
        "data": "2026-04-12",
    }

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.editar_gastos_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.patch("/gastos/1", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once()


# =========================================================
# TESTES - DELETE /gastos/{gasto_id}
# =========================================================

def test_excluir_gastos_api_deve_retornar_204_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.excluir_gastos_service",
        return_value=None
    )

    response = client.delete("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_204_NO_CONTENT
    assert response.content == b""
    mock_service.assert_called_once_with(1, 1)


def test_excluir_gastos_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.excluir_gastos_service",
        side_effect=NotFoundError("Gasto não encontrado.")
    )

    response = client.delete("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Gasto não encontrado."
    }
    mock_service.assert_called_once_with(1, 1)


def test_excluir_gastos_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.excluir_gastos_service",
        side_effect=ValueError("ID deve ser maior que zero.")
    )

    response = client.delete("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "ID deve ser maior que zero."
    }
    mock_service.assert_called_once_with(1, 1)


def test_excluir_gastos_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.gasto_routes.excluir_gastos_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.delete("/gastos/1")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once_with(1, 1)