from decimal import Decimal

import pytest
from datetime import date, timedelta
from src.api.schemas.gasto_schema import GastoCreateRequest, GastoUpdateRequest
from src.core.exceptions import FiltroInvalidoError
from src.models.gastos import Gasto
from src.services.gasto_service import consultar_gastos_por_id_service, consultar_gastos_service, criar_gastos_service, editar_gastos_service

#=======================================================================
#=============== Teste de criação de gastos ============================
#=======================================================================

# Teste de criação de gastos com sucesso
def test_criar_gastos_service_sucesso(mocker):
    gasto_mock = Gasto(
        id=1,
        nome="Mercado",
        valor=Decimal("10.50"),
        categoria="Alimentação",
        descricao="Compra de mantimentos para a semana",
        data=date(2026, 4, 10),
        usuario_id=1
    )

    mock_repo = mocker.patch(
        "src.services.gasto_service.inserir_gasto_repository",
        return_value=gasto_mock
    )

    dados = GastoCreateRequest(
        nome="Mercado",
        valor=Decimal("10.50"),
        categoria="Alimentação",
        descricao="Compra de mantimentos para a semana",
        data=date(2026, 4, 10)
    )

    resultado = criar_gastos_service(dados, usuario_id=1)

    mock_repo.assert_called_once()

    gasto_enviado = mock_repo.call_args[0][0]

    assert gasto_enviado.nome == dados.nome
    assert gasto_enviado.valor == dados.valor
    assert gasto_enviado.categoria == dados.categoria
    assert gasto_enviado.descricao == dados.descricao
    assert gasto_enviado.data == dados.data
    assert gasto_enviado.usuario_id == 1

    assert resultado.nome == dados.nome
    assert resultado.valor == dados.valor
    assert resultado.categoria == dados.categoria
    assert resultado.descricao == dados.descricao
    assert resultado.data == dados.data
    assert resultado.usuario_id == 1


#Teste de criação de gasto com dados invalidos
@pytest.mark.parametrize(
    "campo, valor, mensagem_esperada",
    [
        ("nome", "", "O nome do gasto não pode estar em branco"),
        ("nome", "a" * 55, "O nome do gasto não pode ser maior que 41 caracteres."),
        ("valor", Decimal("0.00"), "O valor deve ser maior que zero."),
        ("valor", Decimal("-10.00"), "O valor deve ser maior que zero."),
        ("categoria", "A" * 101, "A categoria não pode ter mais de 50 caracteres."),
        ("descricao", "B" * 305, "A descrição não pode ter mais de 300 caracteres"),
        ("data", date(2050, 1, 1), "A data não pode ser no futuro."),
    ],
    ids=[
        "nome-vazio",
        "nome-grande0",
        "valor-zero",
        "valor-negativo",
        "categoria-longa",
        "descricao-longa",
        "data-no-futuro",
    ]
)
def test_criar_gastos_service_campos_invalidos(mocker, campo, valor, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.gasto_service.inserir_gasto_repository"
    )

    dados_base = {
        "nome": "Mercado",
        "valor": Decimal("10.50"),
        "categoria": "Alimentação",
        "descricao": "Compra de mantimentos para a semana",
        "data": date(2026, 4, 10),
    }

    dados_base[campo] = valor

    dados = GastoCreateRequest(**dados_base)

    with pytest.raises(ValueError, match=mensagem_esperada):
        criar_gastos_service(dados, usuario_id=1)

    mock_repo.assert_not_called()


# Testa id do usuario no gasto.
@pytest.mark.parametrize(
    "usuario_id, mensagem_esperada",
    [
        ("abc", "ID deve ser um número inteiro válido."),
        (None, "ID deve ser um número inteiro válido."),
        (0, "ID deve ser maior que zero."),
        (-1, "ID deve ser maior que zero."),
    ]
)
def test_criar_gastos_service_usuario_id_invalido(mocker, usuario_id, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.gasto_service.inserir_gasto_repository"
    )

    dados = GastoCreateRequest(
        nome="Mercado",
        valor=Decimal("10.50"),
        categoria="",
        descricao="",
        data=date(2026, 4, 10),
    )

    with pytest.raises(ValueError, match=mensagem_esperada):
        criar_gastos_service(dados, usuario_id=usuario_id)

    mock_repo.assert_not_called()


#=======================================================================
#=============== Teste de consulta de gastos ===========================
#=======================================================================

# Teste de consulta de gastos com filtros status: sucesso
def test_consultar_gastos_service_com_filtros(mocker):
    gasto_mock = Gasto(
        id=1,
        usuario_id=1,
        nome="Mercado",
        valor=Decimal("80.00"),
        categoria="Alimentação",
        descricao="Compra de mantimentos para a semana.",
        data=date(2026, 4, 10),
    )

    mock_repo = mocker.patch(
        "src.services.gasto_service.consultar_gastos_repository",
        return_value=[gasto_mock]
    )

    gastos = consultar_gastos_service(
        usuario_id=1,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=Decimal("10.50"),
        valor_max=Decimal("200.00"),
        descricao="Compra de mantimentos para a semana.",
        data_inicio=date(2026, 4, 1),
        data_final=date(2026, 4, 10),
    )

    mock_repo.assert_called_once_with(
        usuario_id=1,
        nome="Mercado",
        categoria="Alimentação",
        valor_min=Decimal("10.50"),
        valor_max=Decimal("200.00"),
        descricao="Compra de mantimentos para a semana.",
        data_inicio=date(2026, 4, 1),
        data_final=date(2026, 4, 10),
    )

    assert "gastos" in gastos
    assert "quantidade" in gastos
    assert "total" in gastos

    assert gastos["quantidade"] == 1
    assert gastos["total"] == Decimal("80.00")
    assert len(gastos["gastos"]) == 1

    gasto = gastos["gastos"][0]

    assert gasto.usuario_id == 1
    assert gasto.nome == "Mercado"
    assert gasto.categoria == "Alimentação"
    assert gasto.valor == Decimal("80.00")
    assert gasto.descricao == "Compra de mantimentos para a semana."
    assert gasto.data == date(2026, 4, 10)


# Teste para cosultar gastos parametrizado com valores invalidos.
@pytest.mark.parametrize(
    "valor_min, valor_max, data_inicio, data_final, mensagem_esperada",
    [
        (Decimal("-10"), Decimal("100"), None, None, "Valor mínimo inválido."),
        (Decimal("10"), Decimal("-100"), None, None, "Valor máximo inválido."),
        (Decimal("200"), Decimal("100"), None, None, "Valor mínimo não pode ser maior que valor máximo."),
        ("abc", Decimal("100"), None, None, "Valor mínimo inválido."),
        (Decimal("10"), "abc", None, None, "Valor máximo inválido."),
        (None, None, date(2026, 4, 10), date(2026, 4, 1), "Data inicial não pode ser maior que data final."),
    ]
)
def test_consultar_gastos_service_filtros_invalidos(
    mocker,
    valor_min,
    valor_max,
    data_inicio,
    data_final,
    mensagem_esperada
):
    mocker.patch(
        "src.services.gasto_service.consultar_gastos_repository"
    )

    with pytest.raises(FiltroInvalidoError, match=mensagem_esperada):
        consultar_gastos_service(
            usuario_id=1,
            nome=None,
            categoria=None,
            valor_min=valor_min,
            valor_max=valor_max,
            descricao=None,
            data_inicio=data_inicio,
            data_final=data_final,
        )


# Teste de consulta de gasto por ID sucesso
def test_consultar_gasto_service_por_id_sucesso(mocker):
    gasto_mock = Gasto(
        id=1,
        usuario_id=1,
        nome="Mercado",
        categoria="Alimentação",
        valor=Decimal("10.50"),
        descricao="Compra de mantimentos para a semana.",
        data=date(2026, 4, 10),
    )

    mock_repo = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository",
        return_value=gasto_mock
    )

    resultado = consultar_gastos_por_id_service(1, 1)

    mock_repo.assert_called_once_with(1)

    assert resultado.id == gasto_mock.id
    assert resultado.nome == gasto_mock.nome
    assert resultado.categoria == gasto_mock.categoria
    assert resultado.valor == gasto_mock.valor
    assert resultado.descricao == gasto_mock.descricao
    assert resultado.data == gasto_mock.data


# Teste de consulta de gastos por id parametrizado com entradas invalidas
@pytest.mark.parametrize(
    "gasto_id, mensagem_esperada",
    [
        ("abc", "ID deve ser um número inteiro válido."),
        (None, "ID deve ser um número inteiro válido."),
        (0, "ID deve ser maior que zero."),
        (-1, "ID deve ser maior que zero."),
    ]
)
def test_consultar_gasto_service_por_id_gasto_id_invalido(
    mocker,
    gasto_id,
    mensagem_esperada
):
    mock_repo = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository"
    )

    with pytest.raises(ValueError) as exc:
        consultar_gastos_por_id_service(gasto_id, 1)

    assert str(exc.value) == mensagem_esperada

    mock_repo.assert_not_called()


#Teste de consulta de gastos por id do usuario parametrizado com entradas invalidas
@pytest.mark.parametrize(
    "usuario_id, mensagem_esperada",
    [
        ("abc", "ID deve ser um número inteiro válido."),
        (None, "ID deve ser um número inteiro válido."),
        (0, "ID deve ser maior que zero."),
        (-1, "ID deve ser maior que zero."),
    ]
)
def test_consultar_gasto_service_por_id_usuario_id_invalido(
    mocker,
    usuario_id,
    mensagem_esperada
):
    mock_repo = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository"
    )

    with pytest.raises(ValueError) as exc:
        consultar_gastos_por_id_service(1, usuario_id)

    assert str(exc.value) == mensagem_esperada

    mock_repo.assert_not_called()

#=======================================================================
#=============== Teste de editara de gastos ============================
#=======================================================================

# Teste para editar gasto com parametros validos
def test_editar_gastos_service_sucesso(mocker):
    data_valida = date.today() - timedelta(days=1)

    gasto_atual_mock = Gasto(
        id=1,
        usuario_id=1,
        nome="Mercado",
        valor=Decimal("50.00"),
        categoria="Alimentação",
        descricao="Compra antiga",
        data=data_valida,
    )

    gasto_editado_mock = Gasto(
        id=1,
        usuario_id=1,
        nome="Supermercado",
        valor=Decimal("80.00"),
        categoria="Alimentação",
        descricao="Compra atualizada",
        data=data_valida,
    )

    dados = GastoUpdateRequest(
        nome="Supermercado",
        valor=Decimal("80.00"),
        categoria=None,
        descricao="Compra atualizada",
        data=data_valida,
    )

    mock_validar_id = mocker.patch(
        "src.services.gasto_service.validar_id_gasto",
        return_value=1
    )

    mock_consultar = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository",
        return_value=gasto_atual_mock
    )

    mock_editar = mocker.patch(
        "src.services.gasto_service.editar_gasto_repository",
        return_value=gasto_editado_mock
    )

    resultado = editar_gastos_service(
        gasto_id=1,
        dados=dados,
        usuario_id=1,
    )

    mock_validar_id.assert_called_once_with(1)
    mock_consultar.assert_called_once_with(1, 1)
    mock_editar.assert_called_once()

    gasto_enviado = mock_editar.call_args[0][0]

    assert gasto_enviado.id == 1
    assert gasto_enviado.usuario_id == 1
    assert gasto_enviado.nome == "Supermercado"
    assert gasto_enviado.valor == Decimal("80.00")
    assert gasto_enviado.categoria == "Alimentação"
    assert gasto_enviado.descricao == "Compra atualizada"
    assert gasto_enviado.data == data_valida

    assert resultado.id == gasto_editado_mock.id
    assert resultado.usuario_id == gasto_editado_mock.usuario_id
    assert resultado.nome == gasto_editado_mock.nome
    assert resultado.valor == gasto_editado_mock.valor
    assert resultado.categoria == gasto_editado_mock.categoria
    assert resultado.descricao == gasto_editado_mock.descricao
    assert resultado.data == gasto_editado_mock.data


# Teste de edição de gastos parametrizado com campos invalidos
@pytest.mark.parametrize(
    "dados, mensagem_esperada",
    [
        (GastoUpdateRequest(nome=""), "O nome do gasto não pode estar em branco"),
        (GastoUpdateRequest(nome="a" * 101), "O nome do gasto não pode ser maior que 41 caracteres."),
        (GastoUpdateRequest(valor=Decimal("0")), "O valor deve ser maior que zero."),
        (GastoUpdateRequest(valor=Decimal("-10.00")), "O valor deve ser maior que zero."),
        (GastoUpdateRequest(categoria="a" * 51), "A categoria não pode ter mais de 50 caracteres."),
        (GastoUpdateRequest(descricao="a" * 305), "A descrição não pode ter mais de 300 caracteres"),
        (GastoUpdateRequest(data=date(2099, 1, 1)), "A data não pode ser no futuro."),
    ]
)
def test_editar_gastos_service_campos_invalidos(
    mocker,
    dados,
    mensagem_esperada
):
    gasto_atual_mock = Gasto(
        id=1,
        usuario_id=1,
        nome="Mercado",
        valor=Decimal("50.00"),
        categoria="Alimentação",
        descricao="Compra antiga",
        data=date(2026, 4, 10),
    )

    mock_consultar = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository",
        return_value=gasto_atual_mock
    )

    mock_editar = mocker.patch(
        "src.services.gasto_service.editar_gasto_repository"
    )

    with pytest.raises(ValueError) as exc:
        editar_gastos_service(
            gasto_id=1,
            dados=dados,
            usuario_id=1,
        )

    assert str(exc.value) == mensagem_esperada

    mock_consultar.assert_called_once_with(1, 1)
    mock_editar.assert_not_called()


# Teste de edição de gastos parametrizado com gasto_id invalido
@pytest.mark.parametrize(
    "gasto_id, mensagem_esperada",
    [
        ("abc", "ID deve ser um número inteiro válido."),
        (None, "ID deve ser um número inteiro válido."),
        (0, "ID deve ser maior que zero."),
        (-1, "ID deve ser maior que zero."),
    ]
)
def test_editar_gastos_service_gasto_id_invalido(
    mocker,
    gasto_id,
    mensagem_esperada
):
    mock_consultar = mocker.patch(
        "src.services.gasto_service.consultar_gasto_por_id_repository"
    )

    mock_editar = mocker.patch(
        "src.services.gasto_service.editar_gasto_repository"
    )

    dados = GastoUpdateRequest(nome="Novo nome")

    with pytest.raises(ValueError) as exc:
        editar_gastos_service(
            gasto_id=gasto_id,
            dados=dados,
            usuario_id=1,
        )

    assert str(exc.value) == mensagem_esperada

    mock_consultar.assert_not_called()
    mock_editar.assert_not_called()
