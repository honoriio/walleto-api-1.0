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
        "pid": 1234,
        "url": "http://localhost:8501",
        "ativo": True
    }

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )

    mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        return_value=caminho_mock
    )

    mock_iniciar = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard",
        return_value=retorno_dashboard
    )

    resultado = iniciar_dashboard_com_exportacao(usuario_id)

    # valida fluxo completo (orquestração)
    mock_iniciar.assert_called_once()

    kwargs = mock_iniciar.call_args.kwargs
    assert "caminho_arquivo" in kwargs
    assert Path(kwargs["caminho_arquivo"]) == caminho_mock

    assert resultado == retorno_dashboard


# =========================================================
# SEM DADOS
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_lancar_erro_quando_nao_houver_gastos(mocker):
    usuario_id = 1

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": []}
    )

    mock_export = mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel"
    )

    mock_start = mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard"
    )

    with pytest.raises(ValueError, match="Não há gastos para gerar o dashboard"):
        iniciar_dashboard_com_exportacao(usuario_id)

    mock_export.assert_not_called()
    mock_start.assert_not_called()


# =========================================================
# GASTOS = None
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_lancar_erro_quando_gastos_for_none(mocker):
    usuario_id = 1

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": None}
    )

    mocker.patch("src.services.dashboard_service.exportar_gastos_excel")
    mocker.patch("src.services.dashboard_service.iniciar_dashboard")

    with pytest.raises(ValueError, match="Não há gastos para gerar o dashboard"):
        iniciar_dashboard_com_exportacao(usuario_id)


# =========================================================
# ERRO NA CONSULTA
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_da_consulta(mocker):
    usuario_id = 1

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        side_effect=Exception("erro na consulta")
    )

    mocker.patch("src.services.dashboard_service.exportar_gastos_excel")
    mocker.patch("src.services.dashboard_service.iniciar_dashboard")

    with pytest.raises(Exception, match="erro na consulta"):
        iniciar_dashboard_com_exportacao(usuario_id)


# =========================================================
# ERRO NO EXPORT EXCEL
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_do_exportador_excel(mocker):
    usuario_id = 1

    gastos_mock = [{"id": 1, "nome": "Mercado", "valor": 100}]

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )

    mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        side_effect=Exception("erro ao exportar excel")
    )

    mocker.patch("src.services.dashboard_service.iniciar_dashboard")

    with pytest.raises(Exception, match="erro ao exportar excel"):
        iniciar_dashboard_com_exportacao(usuario_id)


# =========================================================
# ERRO NO START DASHBOARD
# =========================================================

def test_iniciar_dashboard_com_exportacao_deve_propagar_erro_ao_iniciar_dashboard(mocker):
    usuario_id = 1

    gastos_mock = [{"id": 1, "nome": "Mercado", "valor": 100}]
    caminho_mock = Path("/tmp/gastos_dashboard.xlsx")

    mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )

    mocker.patch(
        "src.services.dashboard_service.exportar_gastos_excel",
        return_value=caminho_mock
    )

    mocker.patch(
        "src.services.dashboard_service.iniciar_dashboard",
        side_effect=Exception("erro ao iniciar dashboard")
    )

    with pytest.raises(Exception, match="erro ao iniciar dashboard"):
        iniciar_dashboard_com_exportacao(usuario_id)