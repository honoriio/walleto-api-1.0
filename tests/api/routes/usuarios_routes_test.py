import pytest
from fastapi import HTTPException
from starlette import status as http_status

from src.api.main import app
from src.api.routes.usuarios_routes import get_current_user, desativar_usuario_api
from src.core.exceptions import ConflictError, NotFoundError


class DummyUser:
    def __init__(
        self,
        id=1,
        nome="Diego",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha_hash="hash123",
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.senha_hash = senha_hash


def override_get_current_user():
    return DummyUser()


# =========================================================
# TESTES - POST /usuario/
# =========================================================

def test_criar_usuario_api_deve_retornar_201_quando_sucesso(client, mocker):
    payload = {
        "nome": "Diego",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
        "senha": "Senha123"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.criar_usuario_service",
        return_value=DummyUser(
            id=1,
            nome="Diego",
            email="diego@gmail.com",
            data_nascimento="1997-05-21",
            sexo="Masculino",
        )
    )

    response = client.post("/usuario/", json=payload)

    assert response.status_code == http_status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "nome": "Diego",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
    }
    mock_service.assert_called_once()


def test_criar_usuario_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    payload = {
        "nome": "",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
        "senha": "Senha123"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.criar_usuario_service",
        side_effect=ValueError("O nome não pode estar vazio.")
    )

    response = client.post("/usuario/", json=payload)

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "O nome não pode estar vazio."
    }
    mock_service.assert_called_once()


def test_criar_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    payload = {
        "nome": "Diego",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
        "senha": "Senha123"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.criar_usuario_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.post("/usuario/", json=payload)

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once()


# =========================================================
# TESTES - GET /usuario/me
# =========================================================

def test_consultar_meu_usuario_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.consultar_usuario_por_id_service",
        return_value=DummyUser(
            id=1,
            nome="Diego",
            email="diego@gmail.com",
            data_nascimento="1997-05-21",
            sexo="Masculino",
        )
    )

    response = client.get("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "nome": "Diego",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
    }
    mock_service.assert_called_once_with(1)


def test_consultar_meu_usuario_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.consultar_usuario_por_id_service",
        side_effect=NotFoundError("Usuário não encontrado.")
    )

    response = client.get("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado."
    }
    mock_service.assert_called_once_with(1)


def test_consultar_meu_usuario_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.consultar_usuario_por_id_service",
        side_effect=ValueError("ID deve ser maior que zero.")
    )

    response = client.get("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "ID deve ser maior que zero."
    }
    mock_service.assert_called_once_with(1)


def test_consultar_meu_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.consultar_usuario_por_id_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.get("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno no servidor"
    }
    mock_service.assert_called_once_with(1)


# =========================================================
# TESTES - PATCH /usuario/me
# =========================================================

def test_editar_usuario_api_deve_retornar_200_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Diego Atualizado",
        "email": "diego.atualizado@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.editar_usuario_service",
        return_value=DummyUser(
            id=1,
            nome="Diego Atualizado",
            email="diego.atualizado@gmail.com",
            data_nascimento="1997-05-21",
            sexo="Masculino",
        )
    )

    response = client.patch("/usuario/me", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "nome": "Diego Atualizado",
        "email": "diego.atualizado@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
    }
    mock_service.assert_called_once()


def test_editar_usuario_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Diego Atualizado"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.editar_usuario_service",
        side_effect=NotFoundError("Usuário não encontrado.")
    )

    response = client.patch("/usuario/me", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado."
    }
    mock_service.assert_called_once()


def test_editar_usuario_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": ""
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.editar_usuario_service",
        side_effect=ValueError("O nome não pode estar vazio.")
    )

    response = client.patch("/usuario/me", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "O nome não pode estar vazio."
    }
    mock_service.assert_called_once()


def test_editar_usuario_api_deve_retornar_409_quando_service_lancar_conflict_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "email": "jaexiste@gmail.com"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.editar_usuario_service",
        side_effect=ConflictError("E-mail já está em uso.")
    )

    response = client.patch("/usuario/me", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "E-mail já está em uso."
    }
    mock_service.assert_called_once()


def test_editar_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "nome": "Diego Atualizado"
    }

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.editar_usuario_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.patch("/usuario/me", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once()


# =========================================================
# TESTES - DELETE /usuario/me
# =========================================================

def test_excluir_usuario_api_deve_retornar_204_quando_sucesso(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.excluir_usuario_service",
        return_value=None
    )

    response = client.delete("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_204_NO_CONTENT
    assert response.content == b""
    mock_service.assert_called_once_with(1)


def test_excluir_usuario_api_deve_retornar_400_quando_service_lancar_value_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.excluir_usuario_service",
        side_effect=ValueError("ID deve ser maior que zero.")
    )

    response = client.delete("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "ID deve ser maior que zero."
    }
    mock_service.assert_called_once_with(1)


def test_excluir_usuario_api_deve_retornar_404_quando_service_lancar_not_found_error(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.excluir_usuario_service",
        side_effect=NotFoundError("Usuário não encontrado.")
    )

    response = client.delete("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado."
    }
    mock_service.assert_called_once_with(1)


def test_excluir_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(client, mocker):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.excluir_usuario_service",
        side_effect=Exception("erro inesperado")
    )

    response = client.delete("/usuario/me")

    app.dependency_overrides.clear()

    assert response.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Erro interno do servidor."
    }
    mock_service.assert_called_once_with(1)


# =========================================================
# TESTE DIRETO DA FUNÇÃO - desativar_usuario_api
# =========================================================

def test_desativar_usuario_api_deve_retornar_response_204_quando_sucesso(mocker):
    current_user = DummyUser(id=1)

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.desativar_usuario_service",
        return_value=None
    )

    response = desativar_usuario_api(current_user=current_user)

    assert response.status_code == http_status.HTTP_204_NO_CONTENT
    mock_service.assert_called_once_with(1)


def test_desativar_usuario_api_deve_retornar_400_quando_service_lancar_value_error(mocker):
    current_user = DummyUser(id=1)

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.desativar_usuario_service",
        side_effect=ValueError("ID deve ser maior que zero.")
    )

    with pytest.raises(HTTPException) as exc:
        desativar_usuario_api(current_user=current_user)

    assert exc.value.status_code == http_status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "ID deve ser maior que zero."
    mock_service.assert_called_once_with(1)


def test_desativar_usuario_api_deve_retornar_404_quando_service_lancar_not_found_error(mocker):
    current_user = DummyUser(id=1)

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.desativar_usuario_service",
        side_effect=NotFoundError("Usuário não encontrado.")
    )

    with pytest.raises(HTTPException) as exc:
        desativar_usuario_api(current_user=current_user)

    assert exc.value.status_code == http_status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Usuário não encontrado."
    mock_service.assert_called_once_with(1)


def test_desativar_usuario_api_deve_retornar_500_quando_ocorrer_erro_inesperado(mocker):
    current_user = DummyUser(id=1)

    mock_service = mocker.patch(
        "src.api.routes.usuarios_routes.desativar_usuario_service",
        side_effect=Exception("erro inesperado")
    )

    with pytest.raises(HTTPException) as exc:
        desativar_usuario_api(current_user=current_user)

    assert exc.value.status_code == http_status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == "Erro interno do servidor."
    mock_service.assert_called_once_with(1)