import re 
from datetime import date, datetime

def nome_usuario(nome: str) -> str: 
        nome = nome.strip()
            
        if not nome: # --> VALIDAÇÃO 1, VERIFICA SE A STRING ESTA VAZIA
            raise ValueError("O nome não pode estar vazio.")
            
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
        

def validar_sexo_usuario(sexo: str)-> str:
    sexo = sexo.strip().lower()

    if not sexo:
        raise ValueError("O sexo não pode estar vazio")
    
    if sexo not in ["M", "F"]:
        raise ValueError("Sexo inválido. Use 'M' ou 'F'.")
    
    return sexo


def validar_data_nascimento_usuario(data_nascimento: str) -> date:
    data_atual = date.today()
    data_nascimento = data_nascimento.strip()

    if not data_nascimento:
        raise ValueError("A data de nascimento é obrigatória.")

    if len(data_nascimento) == 8 and data_nascimento.isdigit():
        data_nascimento = f"{data_nascimento[0:2]}/{data_nascimento[2:4]}/{data_nascimento[4:8]}"

    data_nascimento = (
        data_nascimento
        .replace(".", "/")
        .replace("-", "/")
        .replace("_", "/")
    )

    try:
        data_nasc_obj = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Formato de data inválido ou data inexistente. Use DD/MM/AAAA.")

    if data_nasc_obj > data_atual:
        raise ValueError("A data de nascimento não pode ser no futuro.")

    idade = data_atual.year - data_nasc_obj.year
    if (data_atual.month, data_atual.day) < (data_nasc_obj.month, data_nasc_obj.day):
        idade -= 1

    if idade > 120:
        raise ValueError("Idade inválida. Verifique a data informada.")

    return data_nasc_obj
