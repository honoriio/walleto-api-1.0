import pytest
from pathlib import Path

from src.services.dashboard_service import iniciar_dashboard_com_exportacao


# =========================================================
# TESTES - iniciar_dashboard_com_exportacao
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_exportar_e_iniciar_dashboard_quando_houver_gastos(mocker):
    usuario_id = 1
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100},
        {"id": 2, "nome": "Transporte", "valor": 50},
    ]
    caminho_mock = Path("/tmp/gastos_dashboard.xlsx")
    retorno_dashboard = {
        "mensagem": "Dashboard iniciado com sucesso.",
        "arquivo": str(caminho_mock)
    }

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        return_value=caminho_mock
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard",
        return_value=retorno_dashboard
    )

    resultado = iniciar_dashboard_com_exportacao(usuario_id)

    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_called_once_with(gastos_mock)
    mock_iniciar_dashboard.assert_called_once_with(caminho_arquivo=caminho_mock)

    assert resultado == retorno_dashboard


def test_iniciar_dashboard_com_exportacao_deve_lancar_erro_quando_nao_houver_gastos(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": []}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel"
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard"
    )

    with pytest.raises(ValueError) as exc:
        iniciar_dashboard_com_exportacao(usuario_id)

    assert str(exc.value) == "Não há gastos para gerar o dashboard."
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_not_called()
    mock_iniciar_dashboard.assert_not_called()


def test_iniciar_dashboard_com_exportacao_deve_lancar_erro_quando_gastos_for_none(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": None}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel"
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard"
    )

    with pytest.raises(ValueError) as exc:
        iniciar_dashboard_com_exportacao(usuario_id)

    assert str(exc.value) == "Não há gastos para gerar o dashboard."
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_not_called()
    mock_iniciar_dashboard.assert_not_called()


def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_da_consulta(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        side_effect=Exception("erro na consulta")
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel"
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard"
    )

    with pytest.raises(Exception) as exc:
        iniciar_dashboard_com_exportacao(usuario_id)

    assert str(exc.value) == "erro na consulta"
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_not_called()
    mock_iniciar_dashboard.assert_not_called()


def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_do_exportador_excel(mocker):
    usuario_id = 1
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100}
    ]

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        side_effect=Exception("erro ao exportar excel")
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard"
    )

    with pytest.raises(Exception) as exc:
        iniciar_dashboard_com_exportacao(usuario_id)

    assert str(exc.value) == "erro ao exportar excel"
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_called_once_with(gastos_mock)
    mock_iniciar_dashboard.assert_not_called()


def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_ao_iniciar_dashboard(mocker):
    usuario_id = 1
    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100}
    ]
    caminho_mock = Path("/tmp/gastos_dashboard.xlsx")

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )
    mock_exportar_excel = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        return_value=caminho_mock
    )
    mock_iniciar_dashboard = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard",
        side_effect=Exception("erro ao iniciar dashboard")
    )

    with pytest.raises(Exception) as exc:
        iniciar_dashboard_com_exportacao(usuario_id)

    assert str(exc.value) == "erro ao iniciar dashboard"
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    mock_exportar_excel.assert_called_once_with(gastos_mock)
    mock_iniciar_dashboard.assert_called_once_with(caminho_arquivo=caminho_mock)