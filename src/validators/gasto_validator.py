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
            

def validar_valor_gasto(valor: Decimal) -> Decimal:
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


def validar_data_gasto(data_str: str) -> date:
    if not data_str or not str(data_str).strip():
        return date.today()

    data_str = str(data_str).strip()

    try:
        # caso: 01012024
        if len(data_str) == 8 and data_str.isdigit():
            data_str = f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"   

        # limpa separadores estranhos
        data_limpa = re.sub(r"\D+", "/", data_str)

        data_obj = datetime.strptime(data_limpa, "%d/%m/%Y").date()

        return data_obj

    except ValueError:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA.")
            

def validar_id_gasto(valor) -> int:
    try:
        numero = int(valor)

        if numero <= 0:
            raise ValueError("ID deve ser maior que zero.")

        return numero

    except (TypeError, ValueError):
        raise ValueError("ID deve ser um número inteiro válido.")
