import pytest
from datetime import date
from src.api.schemas.usuario_schema import UsuarioCreateRequest
from src.models.usuario import Usuario
from src.services.usuario_service import criar_usuario_service


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
#============== Teste de Busca de usuario por ID =======================
#=======================================================================


