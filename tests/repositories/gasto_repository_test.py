import pytest
from decimal import Decimal
from datetime import date

from src.models.gastos import Gasto
from src.repositories.gasto_repository import (
    inserir_gasto_repository,
    consultar_gastos_repository,
    consultar_gasto_por_id_repository,
    editar_gasto_repository,
    excluir_gasto_repository,
)


# =========================================================
# TESTES - inserir_gasto_repository
# =========================================================

def test_inserir_gasto_repository_deve_inserir_gasto_e_retornar_com_id(mocker):
    gasto = Gasto(
        id=None,
        nome="Mercado",
        valor=Decimal("150.50"),
        categoria="Alimentação",
        descricao="Compra do mês",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = {"id": 10}

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = inserir_gasto_repository(gasto)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "INSERT INTO gastos" in args[0]
    assert args[1] == (
        gasto.nome,
        gasto.valor,
        gasto.categoria,
        gasto.descricao,
        gasto.data,
        gasto.usuario_id,
    )

    mock_cursor.fetchone.assert_called_once()
    mock_conn.commit.assert_called_once()

    assert gasto.id == 10
    assert resultado == gasto


def test_inserir_gasto_repository_deve_propagar_erro_do_execute(mocker):
    gasto = Gasto(
        id=None,
        nome="Mercado",
        valor=Decimal("150.50"),
        categoria="Alimentação",
        descricao="Compra do mês",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao inserir gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        inserir_gasto_repository(gasto)

    assert str(exc.value) == "erro ao inserir gasto"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_not_called()
    mock_conn.commit.assert_not_called()


def test_inserir_gasto_repository_deve_propagar_erro_do_fetchone(mocker):
    gasto = Gasto(
        id=None,
        nome="Mercado",
        valor=Decimal("150.50"),
        categoria="Alimentação",
        descricao="Compra do mês",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.side_effect = Exception("erro ao buscar id do gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        inserir_gasto_repository(gasto)

    assert str(exc.value) == "erro ao buscar id do gasto"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
    mock_conn.commit.assert_not_called()


def test_inserir_gasto_repository_deve_propagar_erro_do_commit(mocker):
    gasto = Gasto(
        id=None,
        nome="Mercado",
        valor=Decimal("150.50"),
        categoria="Alimentação",
        descricao="Compra do mês",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = {"id": 10}
    mock_conn.commit.side_effect = Exception("erro ao commitar inserção do gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        inserir_gasto_repository(gasto)

    assert str(exc.value) == "erro ao commitar inserção do gasto"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
    mock_conn.commit.assert_called_once()


# =========================================================
# TESTES - consultar_gastos_repository
# =========================================================

def test_consultar_gastos_repository_deve_retornar_lista_de_gastos_sem_filtros(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchall.return_value = [
        {
            "id": 2,
            "nome": "Transporte",
            "valor": Decimal("50.00"),
            "categoria": "Mobilidade",
            "descricao": "Uber",
            "data": date(2026, 4, 12),
            "usuario_id": 1,
        },
        {
            "id": 1,
            "nome": "Mercado",
            "valor": Decimal("100.00"),
            "categoria": "Alimentação",
            "descricao": "Compra",
            "data": date(2026, 4, 11),
            "usuario_id": 1,
        },
    ]

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_gastos_repository(usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "SELECT id, nome, valor, categoria, descricao, data, usuario_id" in args[0]
    assert "WHERE usuario_id = %s" in args[0]
    assert "ORDER BY data DESC, id DESC" in args[0]
    assert args[1] == (usuario_id,)

    mock_cursor.fetchall.assert_called_once()

    assert isinstance(resultado, list)
    assert len(resultado) == 2
    assert all(isinstance(gasto, Gasto) for gasto in resultado)
    assert resultado[0].id == 2
    assert resultado[1].id == 1


def test_consultar_gastos_repository_deve_aplicar_todos_os_filtros_corretamente(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchall.return_value = []

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_gastos_repository(
        usuario_id=usuario_id,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=Decimal("10.00"),
        valor_max=Decimal("500.00"),
        descricao="Compra",
        data_inicio="2026-04-01",
        data_final="2026-04-30",
    )

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "AND nome ILIKE %s" in args[0]
    assert "AND categoria = %s" in args[0]
    assert "AND valor >= %s" in args[0]
    assert "AND valor <= %s" in args[0]
    assert "AND descricao ILIKE %s" in args[0]
    assert "AND data >= %s" in args[0]
    assert "AND data <= %s" in args[0]
    assert "ORDER BY data DESC, id DESC" in args[0]

    assert args[1] == (
        usuario_id,
        "%Mercado%",
        "Alimentação",
        Decimal("10.00"),
        Decimal("500.00"),
        "%Compra%",
        "2026-04-01",
        "2026-04-30",
    )

    assert resultado == []


def test_consultar_gastos_repository_deve_retornar_lista_vazia_quando_nao_houver_resultados(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchall.return_value = []

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_gastos_repository(usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()
    assert resultado == []


def test_consultar_gastos_repository_deve_propagar_erro_do_execute(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao consultar gastos")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        consultar_gastos_repository(usuario_id=usuario_id)

    assert str(exc.value) == "erro ao consultar gastos"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_not_called()


def test_consultar_gastos_repository_deve_propagar_erro_do_fetchall(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchall.side_effect = Exception("erro ao buscar lista de gastos")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        consultar_gastos_repository(usuario_id=usuario_id)

    assert str(exc.value) == "erro ao buscar lista de gastos"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()


# =========================================================
# TESTES - consultar_gasto_por_id_repository
# =========================================================

def test_consultar_gasto_por_id_repository_deve_retornar_gasto_quando_encontrado(mocker):
    gasto_id = 1
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "nome": "Mercado",
        "valor": Decimal("100.00"),
        "categoria": "Alimentação",
        "descricao": "Compra",
        "data": date(2026, 4, 12),
        "usuario_id": 1,
    }

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_gasto_por_id_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "SELECT id, nome, valor, categoria, descricao, data, usuario_id" in args[0]
    assert "WHERE id = %s AND usuario_id = %s" in args[0]
    assert args[1] == (gasto_id, usuario_id)

    mock_cursor.fetchone.assert_called_once()

    assert isinstance(resultado, Gasto)
    assert resultado.id == 1
    assert resultado.nome == "Mercado"
    assert resultado.valor == Decimal("100.00")


def test_consultar_gasto_por_id_repository_deve_retornar_none_quando_nao_encontrado(mocker):
    gasto_id = 999
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = None

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_gasto_por_id_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
    assert resultado is None


def test_consultar_gasto_por_id_repository_deve_propagar_erro_do_execute(mocker):
    gasto_id = 1
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao consultar gasto por id")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        consultar_gasto_por_id_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    assert str(exc.value) == "erro ao consultar gasto por id"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_not_called()


# =========================================================
# TESTES - editar_gasto_repository
# =========================================================

def test_editar_gasto_repository_deve_retornar_gasto_quando_edicao_for_realizada(mocker):
    gasto = Gasto(
        id=1,
        nome="Mercado Atualizado",
        valor=Decimal("200.00"),
        categoria="Alimentação",
        descricao="Compra atualizada",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = editar_gasto_repository(gasto)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "UPDATE gastos" in args[0]
    assert args[1] == (
        gasto.nome,
        gasto.valor,
        gasto.categoria,
        gasto.descricao,
        gasto.data,
        gasto.id,
        gasto.usuario_id,
    )

    mock_conn.commit.assert_called_once()
    assert resultado == gasto


def test_editar_gasto_repository_deve_retornar_none_quando_nenhum_registro_for_editado(mocker):
    gasto = Gasto(
        id=999,
        nome="Mercado",
        valor=Decimal("100.00"),
        categoria="Alimentação",
        descricao="Compra",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 0

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = editar_gasto_repository(gasto)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

    assert resultado is None


def test_editar_gasto_repository_deve_propagar_erro_do_execute(mocker):
    gasto = Gasto(
        id=1,
        nome="Mercado",
        valor=Decimal("100.00"),
        categoria="Alimentação",
        descricao="Compra",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao editar gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        editar_gasto_repository(gasto)

    assert str(exc.value) == "erro ao editar gasto"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()


def test_editar_gasto_repository_deve_propagar_erro_do_commit(mocker):
    gasto = Gasto(
        id=1,
        nome="Mercado",
        valor=Decimal("100.00"),
        categoria="Alimentação",
        descricao="Compra",
        data=date(2026, 4, 12),
        usuario_id=1,
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1
    mock_conn.commit.side_effect = Exception("erro ao commitar edição do gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        editar_gasto_repository(gasto)

    assert str(exc.value) == "erro ao commitar edição do gasto"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


# =========================================================
# TESTES - excluir_gasto_repository
# =========================================================

def test_excluir_gasto_repository_deve_retornar_true_quando_gasto_for_excluido(mocker):
    gasto_id = 1
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = excluir_gasto_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "DELETE FROM gastos" in args[0]
    assert "WHERE id = %s AND usuario_id = %s" in args[0]
    assert args[1] == (gasto_id, usuario_id)

    mock_conn.commit.assert_called_once()
    assert resultado is True


def test_excluir_gasto_repository_deve_retornar_false_quando_nenhum_gasto_for_excluido(mocker):
    gasto_id = 999
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 0

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    resultado = excluir_gasto_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    assert resultado is False


def test_excluir_gasto_repository_deve_propagar_erro_do_execute(mocker):
    gasto_id = 1
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao excluir gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        excluir_gasto_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    assert str(exc.value) == "erro ao excluir gasto"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()


def test_excluir_gasto_repository_deve_propagar_erro_do_commit(mocker):
    gasto_id = 1
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1
    mock_conn.commit.side_effect = Exception("erro ao commitar exclusão do gasto")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.gasto_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        excluir_gasto_repository(gasto_id=gasto_id, usuario_id=usuario_id)

    assert str(exc.value) == "erro ao commitar exclusão do gasto"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()