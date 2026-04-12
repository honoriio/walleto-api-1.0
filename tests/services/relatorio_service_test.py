import pytest
from pathlib import Path

from src.services.relatorio_service import (
    exportar_gastos_xlsx_service,
    exportar_gastos_pdf_services,
)


# =========================================================
# TESTES - exportar_gastos_xlsx_service
# =========================================================

def test_exportar_gastos_xlsx_service_deve_exportar_arquivo_quando_houver_gastos(mocker):
    usuario_id = 1
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100},
        {"id": 2, "nome": "Transporte", "valor": 50},
    ]
    caminho_mock = Path("/tmp/gastos.xlsx")

    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_excel",
        return_value=caminho_mock
    )

    resultado = exportar_gastos_xlsx_service(
        usuario_id=usuario_id,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=10,
        valor_max=500,
        descricao="compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )

    mock_consultar.assert_called_once_with(
        usuario_id=usuario_id,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=10,
        valor_max=500,
        descricao="compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )
    mock_exportar_excel.assert_called_once_with(gastos_mock)

    assert resultado == {"arquivo": str(caminho_mock)}


def test_exportar_gastos_xlsx_service_deve_lancar_erro_quando_nao_houver_gastos(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": []}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_excel"
    )

    with pytest.raises(ValueError) as exc:
        exportar_gastos_xlsx_service(usuario_id=1)

    assert str(exc.value) == "Não há gastos para exportação."
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_excel.assert_not_called()


def test_exportar_gastos_xlsx_service_deve_lancar_erro_quando_gastos_for_none(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": None}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_excel"
    )

    with pytest.raises(ValueError) as exc:
        exportar_gastos_xlsx_service(usuario_id=1)

    assert str(exc.value) == "Não há gastos para exportação."
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_excel.assert_not_called()


def test_exportar_gastos_xlsx_service_deve_propagar_erro_da_consulta(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        side_effect=Exception("erro na consulta")
    )
    mock_exportar_excel = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_excel"
    )

    with pytest.raises(Exception) as exc:
        exportar_gastos_xlsx_service(usuario_id=1)

    assert str(exc.value) == "erro na consulta"
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_excel.assert_not_called()


def test_exportar_gastos_xlsx_service_deve_propagar_erro_do_exportador(mocker):
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100}
    ]

    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_excel",
        side_effect=Exception("erro ao exportar xlsx")
    )

    with pytest.raises(Exception) as exc:
        exportar_gastos_xlsx_service(usuario_id=1)

    assert str(exc.value) == "erro ao exportar xlsx"
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_excel.assert_called_once_with(gastos_mock)


# =========================================================
# TESTES - exportar_gastos_pdf_services
# =========================================================

def test_exportar_gastos_pdf_services_deve_exportar_arquivo_quando_houver_gastos(mocker):
    usuario_id = 1
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100},
        {"id": 2, "nome": "Transporte", "valor": 50},
    ]
    caminho_mock = Path("/tmp/gastos.pdf")

    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_pdf = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_pdf",
        return_value=caminho_mock
    )

    resultado = exportar_gastos_pdf_services(
        usuario_id=usuario_id,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=10,
        valor_max=500,
        descricao="compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )

    mock_consultar.assert_called_once_with(
        usuario_id=usuario_id,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=10,
        valor_max=500,
        descricao="compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )
    mock_exportar_pdf.assert_called_once_with(gastos_mock)

    assert resultado == {"arquivo": str(caminho_mock)}


def test_exportar_gastos_pdf_services_deve_lancar_erro_quando_nao_houver_gastos(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": []}
    )
    mock_exportar_pdf = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_pdf"
    )

    with pytest.raises(ValueError) as exc:
        exportar_gastos_pdf_services(usuario_id=1)

    assert str(exc.value) == "Não há gastos para exportação."
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_pdf.assert_not_called()


def test_exportar_gastos_pdf_services_deve_lancar_erro_quando_gastos_for_none(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": None}
    )
    mock_exportar_pdf = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_pdf"
    )

    with pytest.raises(ValueError) as exc:
        exportar_gastos_pdf_services(usuario_id=1)

    assert str(exc.value) == "Não há gastos para exportação."
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_pdf.assert_not_called()


def test_exportar_gastos_pdf_services_deve_propagar_erro_da_consulta(mocker):
    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        side_effect=Exception("erro na consulta")
    )
    mock_exportar_pdf = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_pdf"
    )

    with pytest.raises(Exception) as exc:
        exportar_gastos_pdf_services(usuario_id=1)

    assert str(exc.value) == "erro na consulta"
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_pdf.assert_not_called()


def test_exportar_gastos_pdf_services_deve_propagar_erro_do_exportador(mocker):
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100}
    ]

    mock_consultar = mocker.patch(
        "src.services.relatorio_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_pdf = mocker.patch(
        "src.services.relatorio_service.exportar_gastos_pdf",
        side_effect=Exception("erro ao exportar pdf")
    )

    with pytest.raises(Exception) as exc:
        exportar_gastos_pdf_services(usuario_id=1)

    assert str(exc.value) == "erro ao exportar pdf"
    mock_consultar.assert_called_once_with(
        usuario_id=1,
        nome=None,
        categoria=None,
        valor_min=None,
        valor_max=None,
        descricao=None,
        data_inicio=None,
        data_final=None,
    )
    mock_exportar_pdf.assert_called_once_with(gastos_mock)