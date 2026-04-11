# área destinada as importações
from decimal import Decimal
import re
from datetime import date, datetime


def validar_nome_gasto(nome: str)-> str: # --> FUNÇÃO CRIADA PARA COLETAR E VALIDAR NOME  | NO CASO DESTA FUÇÃO E NA COLETA DO NOME, A MESMA ACEITA QALQUER CARACTER, POIS ALGUNS ESTABELECIMENTOS USAM NUMEROS NO NOME.
   nome = nome 

   if not nome: 
       raise ValueError("O nome do gasto não pode estar em branco")
   
   if len(nome) < 4:
       raise ValueError("O nome do gasto não pode ter menor que 4 caracteres.")
   
   if len(nome) >= 41:
       raise ValueError("O nome do gasto não pode ser maior que 41 caracteres.")
   
   return nome.strip()
            

def validar_valor_gasto(valor):
    if not isinstance(valor, Decimal):
        raise ValueError("Valor inválido.")

    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    return valor             
        

def validar_categoria_gasto(categoria: str) -> str:
    if not categoria or not categoria.strip():
        return "Categoria não informada"

    categoria = categoria.strip()

    if len(categoria) > 50:
        raise ValueError("A categoria não pode ter mais de 50 caracteres.")

    if not all(char.isalpha() or char.isspace() for char in categoria):
        raise ValueError("A categoria deve conter apenas letras e espaços.")

    return categoria
            

def validar_descricao_gasto(descricao) -> str:
    descricao = str(descricao).strip()

    if not descricao:
        return "Descrição não informada pelo usuario"

    if len(descricao) > 300:
        raise ValueError("A descrição não pode ter mais de 300 caracteres")

    return descricao


def validar_data_gasto(data_gasto: date | None) -> date:
    hoje = date.today()

    if data_gasto is None:
        return hoje

    if not isinstance(data_gasto, date):
        raise ValueError("Data inválida.")

    if data_gasto > hoje:
        raise ValueError("A data não pode ser no futuro.")

    return data_gasto
            

def validar_id_gasto(valor) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError("ID deve ser um número inteiro válido.")

    if numero <= 0:
        raise ValueError("ID deve ser maior que zero.")

    return numero
