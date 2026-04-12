from decimal import Decimal
from starlette import status as http_status

from src.api.main import app
from src.api.routes.relatorio_routes import get_current_user
from src.core.exceptions import FiltroInvalidoError


class DummyUser:
    def __init__(self, id=1):
        self.id = id


def override_get_current_user():
    return DummyUser(id=1)


# =========================================================
# TESTES - GET /relatorios/exportar/xlsx
# =========================================================

def test_exportar_gastos_xlsx_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    retorno_service = {
        "arquivo": "/tmp/gastos.xlsx"
    }

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_xlsx_service",
        return_value=retorno_service
    )

    response = client.get(
        "/relatorios/exportar/xlsx",
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
        "arquivo": "/tmp/gastos.xlsx"
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


def test_exportar_gastos_xlsx_api_deve_retornar_400_quando_service_lancar_filtro_invalido_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_xlsx_service",
        side_effect=FiltroInvalidoError("Filtro inválido.")
    )

    response = client.get("/relatorios/exportar/xlsx")

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


def test_exportar_gastos_xlsx_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_xlsx_service",
        side_effect=ValueError("Não há gastos para exportação.")
    )

    response = client.get("/relatorios/exportar/xlsx")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Não há gastos para exportação."
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


def test_exportar_gastos_xlsx_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_xlsx_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/relatorios/exportar/xlsx")

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
# TESTES - GET /relatorios/exportar/pdf
# =========================================================

def test_exportar_gastos_pdf_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    retorno_service = {
        "arquivo": "/tmp/gastos.pdf"
    }

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_pdf_services",
        return_value=retorno_service
    )

    response = client.get(
        "/relatorios/exportar/pdf",
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
        "arquivo": "/tmp/gastos.pdf"
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


def test_exportar_gastos_pdf_api_deve_retornar_400_quando_service_lancar_filtro_invalido_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_pdf_services",
        side_effect=FiltroInvalidoError("Filtro inválido.")
    )

    response = client.get("/relatorios/exportar/pdf")

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


def test_exportar_gastos_pdf_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_pdf_services",
        side_effect=ValueError("Não há gastos para exportação.")
    )

    response = client.get("/relatorios/exportar/pdf")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Não há gastos para exportação."
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


def test_exportar_gastos_pdf_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.relatorio_routes.exportar_gastos_pdf_services",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/relatorios/exportar/pdf")

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