# Area destinada a importação
import sys
import os
import platform
import time
from src.core.constants import *
from src.models.gastos import Gasto
from datetime import datetime




def limpar_tela():
    # Verifica o sistema operacional
    if platform.system() == "Windows":
        os.system('cls')  # Comando para Windows
    else:
        os.system('clear')  # Comando para Linux/macOS



def exibir_mensagem(mensagem, cor):
    print(linha("-"))
    print(f'{cor}{mensagem}{RESET}')
    time.sleep(2)



def encerrar_programa():
    limpar_tela()
    print(linha("="))
    print(f'{VERMELHO}PROGRAMA ENCERRADO...{RESET}'.center(CENTRALIZAR))
    print(linha("="))
    time.sleep(2)
    limpar_tela()
    sys.exit()


def extrato(relatorio, saldo): #--> precisamos passar o saldo da conta na hora de chamarmos a função e a lista de transação que e retornada da função obter transações

    print("\nEXTRATO DA CONTA")
    print(linha("-"))

    for t in relatorio:
        print(f"{t['tipo']} | R${t['valor']} | {t['descricao']}")

    print(linha("-"))
    print(f"Saldo atual: R${saldo}")



def mostrar_gasto(gasto: Gasto):
    valor_formatado = f"R$ {gasto.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    #CONVERSÃO DA DATA (ISO → BR)
    try:
        data_formatada = datetime.strptime(gasto.data, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        data_formatada = gasto.data  # fallback caso venha errado

    print(linha("-"))
    print(
        f"{VERDE_CLARO}ID: {gasto.id} | Nome Do Gasto: {gasto.nome} | Valor: {valor_formatado} | "
        f"Categoria: {gasto.categoria} | Descrição: {gasto.descricao} | Data: {data_formatada}{RESET}"
    )
    print(linha("-"))


def exibir_gastos(gastos):
    """Recebe uma lista de gastos e imprime no terminal."""
    if not gastos:
        print("Nenhum gasto encontrado.")
        return

    for gasto in gastos:
        valor_formatado = f"R$ {gasto.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        #CONVERSÃO ISO → BR
        try:
            data_formatada = datetime.strptime(gasto.data, "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            data_formatada = gasto.data

        print(
            f"ID: {gasto.id} | "
            f"Nome: {gasto.nome} | "
            f"Valor: {valor_formatado} | "
            f"Categoria: {gasto.categoria} | "
            f"Descrição: {gasto.descricao} | "
            f"Data: {data_formatada}"
        )
        print(linha("-"))


def exibir_total(total):
    valor_formatado = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(linha("="))
    print(f"Valor Total Gasto: {VERDE}{valor_formatado}{RESET}")


def exibir_mensagem_opcao_invalida():
    print(f"{VERMELHO_CLARO}Opção inválida. Por favor, tente novamente.{RESET}")
    time.sleep(2)

