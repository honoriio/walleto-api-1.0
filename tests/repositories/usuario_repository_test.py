import pytest
from src.repositories.usuario_repository import inserir_usuario_repository
from src.models.usuario import Usuario
from src.models.usuario_auth import UsuarioAuth
from src.repositories.usuario_repository import (
    consultar_usuario_por_id_repository,
    desativar_usuario_repository,
    excluir_usuario_repository,
    consultar_usuario_por_email_repository,
    editar_usuario_repository,
)



#========================================================================================
#================================= Teste de Usuario =====================================
#========================================================================================

#Teste de inserir usuario com sucesso e retornar id.
def test_inserir_usuario_repository_deve_inserir_usuario_e_retornar_com_id(mocker):
    usuario = Usuario(
        id=None,
        nome="Diego",
        email="diego@email.com",
        data_nascimento="1997-01-01",
        sexo="M",
        senha_hash="hash123"
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    # comportamento do cursor
    mock_cursor.fetchone.return_value = {"id": 10}

    # contexto do cursor
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # contexto da conexão
    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )
    mock_conn.__enter__.return_value = mock_conn

    resultado = inserir_usuario_repository(usuario)

    # 1. execute foi chamado corretamente
    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args

    assert "INSERT INTO usuarios" in args[0]

    assert args[1] == (
        usuario.nome,
        usuario.email,
        usuario.data_nascimento,
        usuario.sexo,
        usuario.senha_hash,
    )

    # 2. fetchone foi chamado
    mock_cursor.fetchone.assert_called_once()

    # 3. commit foi chamado
    mock_conn.commit.assert_called_once()

    # 4. id foi atribuído corretamente
    assert usuario.id == 10

    # 5. retorno correto
    assert resultado == usuario


# =========================================================
# TESTES - consultar_usuario_por_id_repository
# =========================================================

def test_consultar_usuario_por_id_repository_deve_retornar_usuario_quando_encontrado(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "nome": "Diego",
        "email": "diego@email.com",
        "data_nascimento": "1997-01-01",
        "sexo": "M",
    }

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_usuario_por_id_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "SELECT id, nome, email, data_nascimento, sexo" in args[0]
    assert args[1] == (usuario_id,)

    mock_cursor.fetchone.assert_called_once()

    assert isinstance(resultado, Usuario)
    assert resultado.id == 1
    assert resultado.nome == "Diego"
    assert resultado.email == "diego@email.com"
    assert resultado.data_nascimento == "1997-01-01"
    assert resultado.sexo == "M"


def test_consultar_usuario_por_id_repository_deve_retornar_none_quando_nao_encontrado(mocker):
    usuario_id = 999

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = None

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_usuario_por_id_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
    assert resultado is None


def test_consultar_usuario_por_id_repository_deve_propagar_erro_do_execute(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao consultar usuario por id")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        consultar_usuario_por_id_repository(usuario_id)

    assert str(exc.value) == "erro ao consultar usuario por id"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_not_called()


# =========================================================
# TESTES - desativar_usuario_repository
# =========================================================

def test_desativar_usuario_repository_deve_retornar_true_quando_usuario_for_desativado(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = desativar_usuario_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "UPDATE usuarios" in args[0]
    assert args[1] == (usuario_id,)
    mock_conn.commit.assert_called_once()

    assert resultado is True


def test_desativar_usuario_repository_deve_retornar_false_quando_nenhum_usuario_for_desativado(mocker):
    usuario_id = 999

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 0

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = desativar_usuario_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

    assert resultado is False


def test_desativar_usuario_repository_deve_propagar_erro_do_execute(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao desativar usuario")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        desativar_usuario_repository(usuario_id)

    assert str(exc.value) == "erro ao desativar usuario"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()


# =========================================================
# TESTES - excluir_usuario_repository
# =========================================================

def test_excluir_usuario_repository_deve_retornar_true_quando_usuario_for_excluido(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = excluir_usuario_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "DELETE FROM usuarios" in args[0]
    assert args[1] == (usuario_id,)
    mock_conn.commit.assert_called_once()

    assert resultado is True


def test_excluir_usuario_repository_deve_retornar_false_quando_nenhum_usuario_for_excluido(mocker):
    usuario_id = 999

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 0

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = excluir_usuario_repository(usuario_id)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

    assert resultado is False


def test_excluir_usuario_repository_deve_propagar_erro_do_execute(mocker):
    usuario_id = 1

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao excluir usuario")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        excluir_usuario_repository(usuario_id)

    assert str(exc.value) == "erro ao excluir usuario"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()


# =========================================================
# TESTES - consultar_usuario_por_email_repository
# =========================================================

def test_consultar_usuario_por_email_repository_deve_retornar_usuario_auth_quando_encontrado(mocker):
    email = "diego@email.com"

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "email": "diego@email.com",
        "senha_hash": "hash123",
    }

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_usuario_por_email_repository(email)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "SELECT id, email, senha_hash" in args[0]
    assert args[1] == (email,)

    mock_cursor.fetchone.assert_called_once()

    assert isinstance(resultado, UsuarioAuth)
    assert resultado.id == 1
    assert resultado.email == "diego@email.com"
    assert resultado.senha_hash == "hash123"


def test_consultar_usuario_por_email_repository_deve_retornar_none_quando_nao_encontrado(mocker):
    email = "naoexiste@email.com"

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.fetchone.return_value = None

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = consultar_usuario_por_email_repository(email)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()

    assert resultado is None


def test_consultar_usuario_por_email_repository_deve_propagar_erro_do_execute(mocker):
    email = "diego@email.com"

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao consultar usuario por email")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        consultar_usuario_por_email_repository(email)

    assert str(exc.value) == "erro ao consultar usuario por email"
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_not_called()


# =========================================================
# TESTES - editar_usuario_repository
# =========================================================

def test_editar_usuario_repository_deve_retornar_usuario_quando_edicao_for_realizada(mocker):
    usuario = Usuario(
        id=1,
        nome="Diego Atualizado",
        email="diego@email.com",
        data_nascimento="1997-01-01",
        sexo="M",
        senha_hash="hash123"
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 1

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = editar_usuario_repository(usuario)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args

    assert "UPDATE usuarios" in args[0]
    assert args[1] == (
        usuario.nome,
        usuario.email,
        usuario.sexo,
        usuario.data_nascimento,
        usuario.id,
    )

    mock_conn.commit.assert_called_once()

    assert resultado == usuario


def test_editar_usuario_repository_deve_retornar_none_quando_nenhum_usuario_for_editado(mocker):
    usuario = Usuario(
        id=999,
        nome="Diego",
        email="diego@email.com",
        data_nascimento="1997-01-01",
        sexo="M",
        senha_hash="hash123"
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.rowcount = 0

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    resultado = editar_usuario_repository(usuario)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

    assert resultado is None


def test_editar_usuario_repository_deve_propagar_erro_do_execute(mocker):
    usuario = Usuario(
        id=1,
        nome="Diego",
        email="diego@email.com",
        data_nascimento="1997-01-01",
        sexo="M",
        senha_hash="hash123"
    )

    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()

    mock_cursor.execute.side_effect = Exception("erro ao editar usuario")

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    mocker.patch(
        "src.repositories.usuario_repository.get_connection",
        return_value=mock_conn
    )

    with pytest.raises(Exception) as exc:
        editar_usuario_repository(usuario)

    assert str(exc.value) == "erro ao editar usuario"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()