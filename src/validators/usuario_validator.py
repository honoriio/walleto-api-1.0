import re 
from datetime import date


def validar_nome_usuario(nome: str) -> str: 
        padrao_nome = r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:\s[A-Za-zÀ-ÖØ-öø-ÿ]+)*$'

        nome = nome.strip()
            
        if not nome: # --> VALIDAÇÃO 1, VERIFICA SE A STRING ESTA VAZIA
            raise ValueError("O nome não pode estar vazio.")
        
        if not re.match(padrao_nome, nome):
            raise ValueError("O nome informado não e valido.")
            
        if len(nome) >= 100: #-->  VALIDAÇÃO 2, O NOME NÃO PODE TER MAIS DE 100 CARACTERES
            raise ValueError("O nome não pode ter mais de 100 caracteres.")

        return nome 


def validar_email_usuario(email: str) -> str:
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' # --> PADRÃO DE CARACTERES QUE É USADO NOS EMAILS.

    email = email.strip()

    if not email: # --> VERIFICA SE A VARIAVEK EMAIL ESTA VAZIA
        raise ValueError("O email não pode estar vazio")
            
    if not re.match(padrao, email):
        raise ValueError("O email informado não é válido.")
    
    return email
        

def validar_sexo_usuario(sexo: str)-> str:   # Temporario, vou arrumar uma solução melhor.
    sexo = sexo.strip().lower()

    if not sexo:
        raise ValueError("O sexo não pode estar vazio")
    
    if sexo not in ["masculino", "feminino"]:
        raise ValueError("Sexo inválido. Use 'Masculino' ou 'Feminino'.")
    
    return sexo.capitalize()


def validar_data_nascimento_usuario(data_nascimento: date) -> date:
    data_atual = date.today()

    if data_nascimento is None:
        raise ValueError("A data de nascimento é obrigatória.")

    if data_nascimento > data_atual:
        raise ValueError("A data de nascimento não pode ser no futuro.")

    idade = data_atual.year - data_nascimento.year
    if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    if idade > 120:
        raise ValueError("Idade inválida. Verifique a data informada.")

    return data_nascimento


def validar_senha_usuario(senha: str) -> str:
    if not isinstance(senha, str):
        raise ValueError("A senha deve ser uma string.")

    senha = senha.strip()

    if not senha:
        raise ValueError("A senha é obrigatória.")

    if len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres.")

    if len(senha.encode("utf-8")) > 72:
        raise ValueError("A senha não pode ter mais de 72 bytes.")

    if not re.search(r"[A-Z]", senha):
        raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")

    if not re.search(r"[a-z]", senha):
        raise ValueError("A senha deve conter pelo menos uma letra minúscula.")

    if not re.search(r"\d", senha):
        raise ValueError("A senha deve conter pelo menos um número.")

    if not re.search(r"[^\w\s]", senha):
        raise ValueError("A senha deve conter pelo menos um caractere especial.")

    return senha



def validar_id_usuario(valor) -> int:
    try:
        numero = int(valor)

        if numero <= 0:
            raise ValueError("ID deve ser maior que zero.")

        return numero

    except (TypeError, ValueError):
        raise ValueError("ID deve ser um número inteiro válido.")