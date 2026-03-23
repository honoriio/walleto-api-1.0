# Área destinada as importações
# --> aqui vai ficar os dados do usuario

class Usuario:
    def __init__(self, nome, email, sexo=None,idade=None, id=None):
        self.nome = nome
        self.email = email
        self.sexo = sexo
        self.idade = idade
        self.id = id
        self.senha_hash = None


        