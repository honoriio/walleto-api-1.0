# área destinada as importações
from decimal import Decimal, InvalidOperation  
import re
import string 
import datetime
from src.models.gastos import Gasto
from src.core.constants import *
from src.repositories.gasto_repository import buscar_gasto_por_id_repository


# Função refatorada, foi tirado o uso sem necessidade de try
def nome_gasto(): # --> FUNÇÃO CRIADA PARA COLETAR E VALIDAR NOME  | NO CASO DESTA FUÇÃO E NA COLETA DO NOME, A MESMA ACEITA QALQUER CARACTER, POIS ALGUNS ESTABELECIMENTOS USAM NUMEROS NO NOME.
    while True:
        print(linha("-"))
        nome = input('Nome do gasto: ').strip()
            
        if not nome: # --> VALIDAÇÃO 1, VERIFICA SE A STRING ESTA VAZIA
            print("O nome não pode estar vazio.")
            continue
            
        if len(nome) >= 41: #-->  VALIDAÇÃO 2, O NOME NÃO PODE TER MAIS DE 40 CARACTERES
            print("O nome não pode ter mais que 40 caracteres.")
            continue
        
        return nome
            

def valor_gasto(): # --> FUNÇÃO QUE COLETA, TRATA E VALIDA O VALOR DO GASTO INFORMADO PELO USUARIO
    while True:
        try:
            print(linha("-"))
            valor = input('Valor: R$ ')
            valor = valor.replace(',', '.')  # --> Substitui a vírgula por ponto
            valor = Decimal(valor)
            if valor <= 0: # --> VALIDAÇÃO 1, O VALOR NÃO PODE SER MENOR OU IGUAL A ZERO. ,,,
                raise ValueError

            return valor
            
        except InvalidOperation:
            print("Por favor, informe um valor numérico válido (ex: 10,50 ou 100).")

        except ValueError:
            print("O valor não pode ser negativo ou menor que zero.")
            
        

def categoria_gasto(): # --> Refatorar essa função e adicionar um menu para escolhas de categorias. 
    while True:
        try:
            print(linha("-"))
            categoria = input('Categoria: ').strip().capitalize()
            if not categoria: # --> CASO O USUARIO NÃO INFORME A CATEGORIA DO GASTO, O PROGRAMA INSERE UMA MENSAGEM GENERICA NA CATEORIA
                categoria = "Categoria não informada"
            
            caracteres_proibidos = string.punctuation + string.digits
            if any(char in caracteres_proibidos for char in categoria): # --> BARRA O USUARIO DE INSERIR CARACTERES E NUMEROS NA CATEGORIA.
                raise ValueError("A categoria deve conter apenas letras.")
            
            if len(categoria) >= 50: # --> O CAMPO CATEGORIA E LIMITADO A 50  CARACTERES.
                raise ValueError("A categoria não pode ser maior que 50 caracteres.")
            
            return categoria
            
        except ValueError as erro:
            print(f"ERRO: {erro}")
            

def descricao_gasto(): # --> COLETA E TRATA O CAMPO DESCRIÇÃO
    while True:
        print(linha("-"))
        descricao = input("Descrição: ").strip()
        if not descricao: # --> CASO O USUARIO NÃO INFPORME UMA DESCRIÇÃO O PROGRAMA IRA INSERIR UMA DESCRIÇÃO GENERICA
            return "Descrição não informada pelo usuario"
            
        if len(descricao) >= 300: # -->  CAMPO DESCRIÇÃO NÃO PODE TER MAIS DE 300 CARACTERES
            print("Descrção não pode ter mais que 300 caracteres.")
            continue

        return descricao



def data_gasto():
    while True:
        try:
            print(linha("-"))
            data_str = input("Data (DD/MM/AAAA): ").strip()
            
            if not data_str:
                return datetime.date.today().strftime("%Y-%m-%d")  #banco

            if len(data_str) == 8 and data_str.isdigit():
                data_str = f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"

            data_limpa = re.sub(r"\D+", "/", data_str)

            data_valida = datetime.datetime.strptime(data_limpa, "%d/%m/%Y").date()
            
            #AQUI É A MUDANÇA IMPORTANTE
            return data_valida.strftime("%Y-%m-%d")

        except ValueError:
            print("ERRO: Formato de data inválido ou data não existe. Use DD/MM/AAAA.")
            


def entrada_gastos(): # --> REUNE TODAS AS FUNÇÕES DE COLETA DE DADOS NA ORDEM CORRETA
    nome = nome_gasto()
    valor = valor_gasto()
    categoria = categoria_gasto()
    descricao = descricao_gasto()
    data = data_gasto()

    return Gasto(nome, valor, categoria, descricao, data)


#======================================================================================================================
#------------------------------- Funções para coletar dados para edição de gasto --------------------------------------
#======================================================================================================================


def solicitar_id_gasto():
    while True:
        print(linha("-"))
        entrada_usuario = input("Informe o id do gasto: ").strip()

        try:
            numero = int(entrada_usuario)

            if numero <= 0:
                print("Erro: ID deve ser maior que zero.")
                continue

            return numero

        except ValueError:
            print("Erro: Por favor, digite apenas números inteiros. Tente novamente.")

def nome_editar_gasto(nome_atual):
    while True:
        print(linha("-"))
        print()
        print(f"{VERDE_CLARO}Nome Atual:{RESET} {AMARELO_CLARO}{nome_atual}{RESET}")
        nome = input(f"Novo nome: ").strip()

        if not nome:
            return nome_atual

        if len(nome) >= 41:
            print("O nome não pode ter mais que 40 caracteres.")
            continue

        return nome 


def valor_editar_gasto(valor_atual):
    while True:
        print()
        print(f"{VERDE_CLARO}Valor Atual: R${RESET}{AMARELO_CLARO}{valor_atual:,.2f}{RESET}")
        valor = input(f"Novo valor R$: ").strip()

        if not valor:
            if isinstance(valor_atual, Decimal):
                return valor_atual

            try:
                return Decimal(str(valor_atual).replace(",", "."))
            except InvalidOperation:
                print("Valor antigo inválido.")
                continue

        try:
            valor_convertido = Decimal(valor.replace(",", "."))
        except InvalidOperation:
            print("Valor inválido.")
            continue

        if valor_convertido <= 0:
            print("O valor deve ser maior que zero.")
            continue

        return valor_convertido


def categoria_editar_gasto(categoria_atual):
    while True:
        try:
            print()
            print(f"{VERDE_CLARO}Categoria Atual:{RESET} {AMARELO_CLARO}{categoria_atual}{RESET}")
            categoria = input(f"Nova categoria: ").strip()

            # mantém categoria antiga
            if not categoria:
                return categoria_atual

            categoria = categoria.capitalize()

            caracteres_proibidos = string.punctuation + string.digits
            if any(char in caracteres_proibidos for char in categoria):
                raise ValueError("A categoria deve conter apenas letras.")

            if len(categoria) >= 50:
                raise ValueError("A categoria não pode ser maior que 50 caracteres.")

            return categoria

        except ValueError as erro:
            print(f"ERRO: {erro}")


def descricao_editar_gasto(descricao_atual):
    while True:
        print()
        print(f"{VERDE_CLARO}Descrição Atual:{RESET} {AMARELO_CLARO}{descricao_atual}{RESET}")
        descricao = input(f"Nova descrição: ").strip()

        # manter descrição antiga
        if not descricao:
            return descricao_atual

        descricao = descricao.lower()

        if len(descricao) >= 300:
            print("Descrição não pode ter mais que 300 caracteres.")
            continue

        return descricao
        

def data_editar_gasto(data_atual):
    while True:
        try:
            data_formatada = datetime.datetime.strptime(data_atual, "%Y-%m-%d").strftime("%d/%m/%Y")
            print()
            print(f"{VERDE_CLARO}Data Atual:{RESET} {AMARELO_CLARO}{data_formatada}{RESET}")
            data_str = input(f"Nova data: ").strip()

            # manter data antiga
            if not data_str:
                return data_atual

            # trata datas sem separadores (DDMMAAAA)
            if len(data_str) == 8 and data_str.isdigit():
                data_str = f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"

            # normaliza separadores
            data_limpa = re.sub(r"\D+", "/", data_str)

            data_valida = datetime.datetime.strptime(data_limpa, "%d/%m/%Y").date()

            return data_valida.strftime("%Y-%m-%d") #--> Retorna a data no padrão ISO

        except ValueError:
            print("ERRO: Formato de data inválido ou data não existe. Use DD/MM/AAAA ou DDMMAAAA.")



def coletar_dados_edicao(gasto):
    nome = nome_editar_gasto(gasto.nome)
    valor = valor_editar_gasto(gasto.valor)
    categoria = categoria_editar_gasto(gasto.categoria)
    descricao = descricao_editar_gasto(gasto.descricao)
    data = data_editar_gasto(gasto.data)

    return {
        "id": gasto.id,
        "nome": nome,
        "valor": valor,
        "categoria": categoria,
        "descricao": descricao,
        "data": data,
    }


def valor_gasto_filtrar(mensagem): # --> FUNÇÃO USADA PARA COLETAR  VALORES PARA BUSCA DE GASTOS COM PERIODO DE VALOR, A MESMA RECEBE UYM STRING PARA A MENSAGEM PARA O USUARIO
    while True:
        try:
            print(linha("-"))
            valor = input(f"{mensagem}")
            valor = valor.replace(',', '.')  # --> Substitui a vírgula por ponto
            valor = Decimal(valor)
            if valor <= 0: # --> VALIDAÇÃO 1, O VALOR NÃO PODE SER MENOR OU IGUAL A ZERO.
                raise ValueError
            
            return valor
            
        except InvalidOperation:
            print("Por favor, informe um valor numérico válido (ex: 10,50 ou 100).")

        except ValueError:
            print("O valor não pode ser negativo ou menor que zero.")
