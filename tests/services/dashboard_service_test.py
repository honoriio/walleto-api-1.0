import pytest
from src.services.dashboard_service import obter_gastos_dashboard


# =========================================================
# TESTES - obter_gastos_dashboard
# =========================================================

def test_obter_gastos_dashboard_deve_retornar_gastos_quando_existirem(mocker):
    usuario_id = 1

    gastos_mock = [
        {"id": 1, "nome": "Mercado", "valor": 100},
        {"id": 2, "nome": "Transporte", "valor": 50},
    ]

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": gastos_mock}
    )

    resultado = obter_gastos_dashboard(usuario_id)

    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    assert resultado == gastos_mock


def test_obter_gastos_dashboard_deve_retornar_lista_vazia_quando_nao_houver_gastos(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": []}
    )

    resultado = obter_gastos_dashboard(usuario_id)

    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    assert resultado == []


def test_obter_gastos_dashboard_deve_retornar_lista_vazia_quando_gastos_for_none(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        return_value={"gastos": None}
    )

    resultado = obter_gastos_dashboard(usuario_id)

    mock_consultar.assert_called_once_with(usuario_id=usuario_id)
    assert resultado == []


def test_obter_gastos_dashboard_deve_propagar_erro_da_consulta(mocker):
    usuario_id = 1

    mock_consultar = mocker.patch(
        "src.services.dashboard_service.consultar_gastos_service",
        side_effect=Exception("erro na consulta")
    )

    with pytest.raises(Exception) as exc:
        obter_gastos_dashboard(usuario_id)

    assert str(exc.value) == "erro na consulta"
    mock_consultar.assert_called_once_with(usuario_id=usuario_id)