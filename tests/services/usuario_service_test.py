import pytest
from datetime import date
from src.api.schemas.usuario_schema import UsuarioCreateRequest, UsuarioUpdateRequest
from src.models.usuario import Usuario
from src.services.usuario_service import consultar_usuario_por_id_service, criar_usuario_service, desativar_usuario_service, editar_usuario_service, excluir_usuario_service


#=======================================================================
#============== Teste de criação de usuario ============================
#=======================================================================

def test_criar_usuario_service_sucesso(mocker):
    usuario_mock = Usuario(
        id=1,
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento=date(1997, 5, 21),
        sexo="Masculino",
        senha_hash="hash_fake",
    )

    mock_repo = mocker.patch(
    "src.services.usuario_service.inserir_usuario_repository",
    return_value=usuario_mock
    )
    

    mocker.patch(
        "src.services.auth_service.gerar_hash_senha",
        return_value="hash_fake"
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha="Di1234567891.",
    )

    resultado = criar_usuario_service(dados)
    mock_repo.assert_called_once()

# Testa se o objeto foi montado corretamente!!! 
#======================================================================
    usuario_enviado = mock_repo.call_args[0][0]

    assert usuario_enviado.nome == dados.nome
    assert usuario_enviado.email == dados.email
    assert usuario_enviado.data_nascimento == dados.data_nascimento
    assert usuario_enviado.sexo == dados.sexo
#=======================================================================
    assert resultado.nome == dados.nome
    assert resultado.email == dados.email
    assert resultado.data_nascimento == dados.data_nascimento
    assert resultado.sexo == dados.sexo


# Teste com Nome do usuário vazio
def test_criar_usuario_service_nome_vazio(mocker):
    mock_repo =  mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )

    dados = UsuarioCreateRequest(
        nome="",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError):
        criar_usuario_service(dados)
    
    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()


# Teste com o email do usuario invalido.
def test_criar_usuario_service_email_invalido(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diegogmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError, match="O email informado não é válido."):
        criar_usuario_service(dados)

    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()
    

# Teste de data invalido, data esta no futuro
# OBS, para teste do service, devemos testar apenas regras de negocio. deixar tipo para o schemas
def test_criar_usuario_service_data_no_futuro(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="2050-01-01",  
        sexo="Masculino",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError, match="A data de nascimento não pode ser no futuro."):
        criar_usuario_service(dados)

    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()


# Teste de sexo invalido (Sem ser masculino ou feminino)
def test_criar_usuario_service_sexo_invalido(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21", 
        sexo="Reptiliano",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError, match="Sexo inválido. Use 'Masculino' ou 'Feminino'."):
        criar_usuario_service(dados)

    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()


# Teste de sexo vazio
def test_criar_usuario_service_sexo_vazio(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21", 
        sexo="",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError, match="O sexo não pode estar vazio"):
        criar_usuario_service(dados)

    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()


# Teste parametrizado para testar varias senhas incorretas.
@pytest.mark.parametrize(
    "senha, mensagem_esperada",
    [
        ("", "A senha é obrigatória."),
        ("123456", "A senha deve ter pelo menos 8 caracteres"),
        ("12345678", "A senha deve conter pelo menos uma letra maiúscula."),
        ("Abcdefgh", "A senha deve conter pelo menos um número."),
        ("1234567A", "A senha deve conter pelo menos uma letra minúscula."),
        ("1234567a", "A senha deve conter pelo menos uma letra maiúscula."),
    ]
)

def test_criar_usuario_service_senhas_invalidas(mocker, senha, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository"
    )
    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha=senha,
    )

    with pytest.raises(ValueError, match=mensagem_esperada):
        criar_usuario_service(dados)

    # verifica se o repository não foi chamado a nenhum momento.
    mock_repo.assert_not_called()


# Teste de email duplicado.
def test_criar_usuario_service_email_duplicado(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.inserir_usuario_repository",
        side_effect=ValueError("E-mail já cadastrado")
    )

    dados = UsuarioCreateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
        senha="Di1234567891.",
    )

    with pytest.raises(ValueError, match="E-mail já cadastrado"):
        criar_usuario_service(dados)

    # verifica se o repository foi de fato chamado.
    mock_repo.assert_called_once()


#=======================================================================
#============== Teste de Consulta de usuario por ID ====================
#=======================================================================

# Testa Uma busca valida de usuaario por id 
def test_consultar_usuario_service_por_id_sucesso(mocker):
    usuario_mock = Usuario(
        id=1,
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento=date(1997, 5, 21),
        sexo="Masculino",
        senha_hash="hash_fake",
    )

    mock_repo = mocker.patch(
        "src.services.usuario_service.consultar_usuario_por_id_repository",
        return_value=usuario_mock
    )

    resultado = consultar_usuario_por_id_service(1)

    mock_repo.assert_called_once_with(1)

    assert resultado.id == usuario_mock.id
    assert resultado.nome == usuario_mock.nome
    assert resultado.email == usuario_mock.email


# Teste de consulta de usuario por ID parametrizado
@pytest.mark.parametrize(
        "usuario_id, mensagem_esperada",
        [
            (0, "ID deve ser um número inteiro válido."),
            ("a", "ID deve ser um número inteiro válido."),
            (-0, "ID deve ser um número inteiro válido.")
        ]
)

# Teste de consulta de usuario por ID com ID = 0
def test_consultar_usuario_service_id(mocker, usuario_id, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.usuario_service.consultar_usuario_por_id_repository"
    )

    with pytest.raises(ValueError, match=mensagem_esperada):
        consultar_usuario_por_id_service(usuario_id)

    mock_repo.assert_not_called()


#=======================================================================
#================== Teste de desativação de usuario ====================
#=======================================================================

# Teste de desativação de usuario por ID valido
def test_desativar_usuario_id_service_sucesso(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.desativar_usuario_repository",
        return_value=True
    )

    resultado = desativar_usuario_service(1)

    mock_repo.assert_called_once_with(1)
    assert resultado is True


# Teste para desativar o usuario com base no ID Parametrizado
@pytest.mark.parametrize(
        "usuario_id, mensagem_esperada",
        [
            (0, "ID deve ser um número inteiro válido."),
            ("a", "ID deve ser um número inteiro válido."),
            (-1, "ID deve ser um número inteiro válido.")
        ]
)


# Teste de consulta de usuario por ID com ID = 0
def test_desativar_usuario_id(mocker, usuario_id, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.usuario_service.desativar_usuario_repository"
    )

    with pytest.raises(ValueError, match=mensagem_esperada):
        desativar_usuario_service(usuario_id)

    mock_repo.assert_not_called()

#=======================================================================
#===================== Teste de exclusão de usuario ====================
#=======================================================================

# Teste de exclusão de usuario por ID
def test_excluir_usuario_service_sucesso(mocker):
    mock_repo = mocker.patch(
        "src.services.usuario_service.excluir_usuario_repository",
        return_value=True
    )

    resultado = excluir_usuario_service(1)

    mock_repo.assert_called_once_with(1)
    assert resultado is True


# Teste para excluir o usuario com base no ID Parametrizado
@pytest.mark.parametrize(
        "usuario_id, mensagem_esperada",
        [
            (0, "ID deve ser um número inteiro válido."),
            ("a", "ID deve ser um número inteiro válido."),
            (-1, "ID deve ser um número inteiro válido.")
        ]
)


# Teste de consulta de usuario por ID com ID = 0
def test_excluir_usuario_id(mocker, usuario_id, mensagem_esperada):
    mock_repo = mocker.patch(
        "src.services.usuario_service.excluir_usuario_repository"
    )

    with pytest.raises(ValueError, match=mensagem_esperada):
        excluir_usuario_service(usuario_id)

    mock_repo.assert_not_called()


#=======================================================================
#===================== Teste de edição de usuario ======================
#=======================================================================

# Teste de editar usuario com sucesso
def test_editar_usuario_service_sucesso(mocker):
    usuario_mock = Usuario(
        id=1,
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento=date(1997, 5, 21),
        sexo="Masculino",
        senha_hash="hash_fake",
    )

    mock_repo = mocker.patch(
        "src.services.usuario_service.editar_usuario_repository",
        return_value=usuario_mock
    )

    dados = UsuarioUpdateRequest(
        nome="Diego Honorio",
        email="diego@gmail.com",
        data_nascimento="1997-05-21",
        sexo="Masculino",
    )

    resultado = editar_usuario_service(1, dados)

    mock_repo.assert_called_once()

    # Valida o objeto enviado ao repository
    usuario_enviado = mock_repo.call_args[0][0]

    assert usuario_enviado.nome == dados.nome
    assert usuario_enviado.email == dados.email
    assert usuario_enviado.data_nascimento == dados.data_nascimento
    assert usuario_enviado.sexo == dados.sexo

    assert resultado.id == 1
    assert resultado.nome == dados.nome
    assert resultado.email == dados.email
    assert resultado.data_nascimento == dados.data_nascimento
    assert resultado.sexo == dados.sexo


#Teste De edição de usuario parametrizado
@pytest.mark.parametrize(
    "campo, valor, mensagem_esperada",
    [
        ("nome", "", "O nome não pode estar vazio."),
        ("email", "diegogmail.com", "O email informado não é válido."),
        ("sexo", "Reptiliano", "Sexo inválido."),
        ("data_nascimento", "2050-01-01", "A data de nascimento não pode ser no futuro."),
    ]
)

def test_editar_usuario_service_campos_invalidos(mocker, campo, valor, mensagem_esperada):

    mock_repo = mocker.patch(
        "src.services.usuario_service.editar_usuario_repository"
    )

    dados_base = {
        "nome": "Diego Honorio",
        "email": "diego@gmail.com",
        "data_nascimento": "1997-05-21",
        "sexo": "Masculino",
    }

    dados_base[campo] = valor

    dados = UsuarioUpdateRequest(**dados_base)

    with pytest.raises(ValueError, match=mensagem_esperada):
        editar_usuario_service(1, dados)

    mock_repo.assert_not_called()

    