# Área destinada as importações
import time
from src.core.constants import *
from decimal import InvalidOperation 
from src.repositories.gasto_repository import buscar_gasto_por_id_repository
from src.views.tela import limpar_tela
from src.views.gastos_views import valor_gasto_filtrar
import string
import datetime 
from src.utils.utils_layer import validar_e_converter_data


def menu_principal():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}WALLETO - MENU PRINCIPAL{RESET}".center(CENTRALIZAR))
    print(linha("="))
    print("[1] - Gerenciar Gastos")
    print("[2] - Consultar Gastos e Relatorios")
    print("[0] - Sair")
    print(linha("-"))
        
    while True:
        try:
            opc_str = input("Opção: ")
            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue
            opc = int(opc_str)
            return opc

        except InvalidOperation:
            print("Por favor, informe um valor numérico válido (ex: 10,50 ou 100).")

        except ValueError:
            print("Digite um valor númerico.")



def menu_gerenciar_gastos():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}GERENCIAR GASTOS{RESET}".center(CENTRALIZAR))
    print(linha("="))
    print("[1] - Adicionar Novo Gasto")
    print("[2] - Editar Gasto")
    print("[3] - Excluir Gasto")
    print("[0] - Voltar ao Menu Principal")
    print(linha("-"))

    while True:
        try:
            opc_str = input("Opção: ")
            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue
            opc = int(opc_str)
            return opc

        except InvalidOperation:
            print("Por favor, informe um valor numérico válido (ex: 10,50 ou 100).")

        except ValueError:
            print("Digite um valor númerico.")



def consultas_e_relatorios():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}CONSULTAS E RELATORIOS{RESET}".center(CENTRALIZAR))
    print(linha("="))
    print("[1] Listar Todos os Gastos")
    print("[2] Buscar Gasto por ID")
    print("[3] Filtrar por Categoria")
    print("[4] Filtrar por Data")
    print("[5] Filtrar por Valor")
    print("[6] Exportar Gastos")
    print("[0] Voltar ao Menu Principal")
    print(linha("-"))

    while True:
        try:
            opc_str = input("Opção: ")
            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue
            opc = int(opc_str)
            return opc

        except InvalidOperation:
            print("Por favor, informe um valor numérico válido (ex: 10,50 ou 100).")

        except ValueError:
            print("Digite um valor númerico.")



def menu_listar_gastos():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}LISTA DE GASTOS{RESET}".center(CENTRALIZAR))
    print(linha("="))

def cabecalho_excluir_gasto():
    limpar_tela() 
    print(linha("="))
    print(f'{VERMELHO}EXCLUIR GASTOS{RESET}'.center(CENTRALIZAR))
    print(linha("="))

    while True:
        # Pede o dado ao usuário usando a mensagem fornecida
        entrada_usuario = input("Informe o id do gasto: ")
        
        try:
            numero = int(entrada_usuario)
            return numero
        
        except ValueError:
            print("Erro: Por favor, digite apenas números inteiros. Tente novamente.")


def cabecalho_buscar_por_id():
    limpar_tela() 
    print(linha("="))
    print(f'{AZUL}BUSCA POR ID{RESET}'.center(CENTRALIZAR))
    print(linha("="))

    while True:
        print(linha("-"))
        entrada_usuario = input("Informe o id do gasto: ")

        try:
            numero = int(entrada_usuario)

            if numero <= 0:
                print("Erro: ID deve ser maior que zero.")
                continue

            gasto = buscar_gasto_por_id_repository(numero)

            if gasto is None:
                print(f"Nenhum gasto encontrado com o ID {numero}.")
                continue

            return numero

        except ValueError:
            print("Erro: Por favor, digite apenas números inteiros. Tente novamente.")



def menu_filtrar_gasto_categoria():
    limpar_tela() 
    print(linha("="))
    print(f'{AMARELO}BUSCAR POR CATEGORIA{RESET}'.center(CENTRALIZAR))
    print(linha("="))

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


def menu_filtrar_data():
    limpar_tela()
    print(linha("="))
    print(f'{VERDE}BUSCA POR DATA{RESET}'.center(CENTRALIZAR))
    print(linha("="))

    while True:
        # --- Obter Data Inicial ---
        try:
            print(linha("-"))
            data_inicio_str = input("Data início (DD/MM/AAAA) [Obrigatório]: ").strip()
            if not data_inicio_str:
                print("ERRO: A data inicial não pode estar em branco. Tente novamente.")
                continue

            data_inicio_obj = validar_e_converter_data(data_inicio_str)

        except ValueError as e:
            print(f"ERRO (Data Início): {e}")
            continue

        # --- Obter Data Final ---
        try:
            print(linha("-"))
            data_final_str = input("Data final (DD/MM/AAAA) [Pressione ENTER para hoje]: ").strip()
            
            if not data_final_str:
                # Se o usuário pressionar Enter, usa a data de hoje como padrão
                data_final_obj = datetime.date.today()
            else:
                data_final_obj = validar_e_converter_data(data_final_str)

        except ValueError as e:
            print(f"ERRO (Data Final): {e}")
            continue
        
        # --- Validação de Intervalo ---
        if data_final_obj < data_inicio_obj:
            print(f"ERRO: A data final ({data_final_obj.strftime('%d/%m/%Y')}) não pode ser anterior à data inicial ({data_inicio_obj.strftime('%d/%m/%Y')}).")
            print(linha("-"))
            continue # Reinicia o processo de solicitação de datas

        
        return data_inicio_obj, data_final_obj
    
# --> Essa função foi refatorada para verificar se o valor maximo e maior que o valor minimo inserido pelo usuario para ser usada para filtrar gasto por valor.
def menu_filtrar_valor(): 
    limpar_tela()
    print(linha("="))
    print(f'{VERDE}BUSCA POR VALOR{RESET}'.center(CENTRALIZAR))
    print(linha("="))

    valor_a = "Valor Inicial: R$ "
    valor_b = "Valor Final: R$ "

    valor_min = valor_gasto_filtrar(valor_a)

    while True:
        valor_max = valor_gasto_filtrar(valor_b)

        if valor_max <= valor_min:
            print(f"O valor máximo deve ser maior que R$ {valor_min}.")
            time.sleep(2)
        else:
            print(linha("="))
            return valor_min, valor_max

def menu_anterior():
    print(linha("="))
    print(f"{VERDE}[0]{RESET} - {AMARELO}VOLTAR AO MENU ANTERIOR{RESET}")
    print(linha("="))
    while True:
        try:    
            opc = int(input("Opção: "))

            if opc != 0:
                raise ValueError
        
            return opc
        
        except ValueError:
            print("Por favor, digite ZERO para voltar ao menu anterior.")




def menu_filtro_exportação():
    print(linha("="))
    print(f"{VERDE_CLARO}[1] Exportar para XLSX{RESET}")
    print(f"{VERDE_CLARO}[2] Abrir dashboard{RESET}")
    print(f"{VERMELHO_CLARO}[0] Voltar{RESET}")
    print(linha("="))
        
    while True:
        try:
            opc_str = input("Opção: ").strip()

            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue
            
            opc = int(opc_str)

            # VALIDAÇÃO DO MENU
            if opc not in (0, 1, 2):
                print("Opção inválida. Escolha 0, 1 ou 2.")
                continue

            return opc

        except ValueError:
            print("Digite um valor numérico válido.")

def menu_adicionar_gastos():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}ADICIONAR GASTOS{RESET}".center(CENTRALIZAR))
    print(linha("="))


def menu_editar_gasto():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}EDITAR GASTOS{RESET}".center(CENTRALIZAR))
    print(linha("="))


def menu_exportacao():
    limpar_tela()
    print(linha("="))
    print(f"{VERDE}EXPORTAÇÃO DE GASTOS{RESET}".center(CENTRALIZAR))
    print(linha("="))

    print("[1] Exportar para XLSX")
    print("[2] Abrir Dashboard")
    print("[3] Exportar para PDF")
    print("[0] Voltar ao menu anterior")
    print(linha("-"))

    OPCOES_VALIDAS = {0, 1, 2, 3}

    while True:
        try:
            opc_str = input("Opção: ").strip()

            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue

            opc = int(opc_str)

            # VALIDAÇÃO DAS OPÇÕES
            if opc not in OPCOES_VALIDAS:
                print("Opção inválida. Escolha 0, 1, 2 ou 3.")
                continue

            return opc

        except ValueError:
            print("Digite um valor numérico válido.")


def confirmar_exclusao():
    print("Deseja realmente excluir o gasto?")
    print()
    print("[1] SIM")
    print("[2] NÃO")
    print(linha("-"))

    OPCOES_VALIDAS = {1, 2}

    while True:
        try:
            opc_str = input("Opção: ").strip()

            if not opc_str:
                print("Digite uma opção, o campo não pode ficar em branco.")
                continue

            opc = int(opc_str)

            # VALIDAÇÃO DAS OPÇÕES
            if opc not in OPCOES_VALIDAS:
                print("Opção inválida. Escolha 1 (SIM) ou 2 (NÃO).")
                continue

            return opc

        except ValueError:
            print("Digite um valor numérico válido.")


"""def menu_categorias(): # --> Ainda irei decidir se devo ou não mudar a forma como adicionam as categorias.
    largura = 29
    categorias = [
    "Alimentação","Mercado","Farmácia","Saúde",
    "Transporte","Combustível","Moradia","Energia",
    "Água","Internet","Telefone","Assinaturas",
    "Educação","Cursos","Lazer","Viagem",
    "Roupas","Beleza","Presentes","Pets",
    "Manutenção","Casa","Impostos","Taxas",
    "Investimentos","Poupança","Doações","Seguros",
    "Trabalho","Outros"
    ]

    print("=" * TM)
    print(f"{AMARELO}CATEGORIAS{RESET}".center(TM))
    print("=" * TM)

    for i in range(0, len(categorias), 2):
        esquerda = f"[{i+1}] - {categorias[i]}"
    
        if i + 1 < len(categorias):
            direita = f"[{i+2}] - {categorias[i+1]}"
        else:
            direita = ""
    
        print(f"{esquerda:<{largura}}| {direita:<{largura}}")"""
