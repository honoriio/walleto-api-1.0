from src.views.menus import menu_principal, menu_gerenciar_gastos, consultas_e_relatorios
from src.views.tela import encerrar_programa, exibir_mensagem_opcao_invalida
from src.core.constants import VERMELHO_CLARO, RESET
from src.core.database import inicializar_banco
from src.views.fluxo_gastos_view import (
    fluxo_adicionar_gasto,
    fluxo_editar_gasto,
    fluxo_excluir_gasto,
    fluxo_listar_gastos,
    fluxo_filtrar_gasto_por_id,
    fluxo_filtrar_gastos_por_categoria,
    fluxo_filtrar_gastos_por_data,
    fluxo_filtrar_gastos_por_valor,
    fluxo_exportacao,
)
import time


def main():
    inicializar_banco()

    while True:
        opc = menu_principal()

        match opc:
            case 1:  # --> GERENCIAR GASTOS
                opc = menu_gerenciar_gastos()

                match opc:
                    case 1:
                        fluxo_adicionar_gasto()

                    case 2:
                        fluxo_editar_gasto()

                    case 3:
                        fluxo_excluir_gasto()

                    case 0:
                        continue

                    case _:
                        print(f"{VERMELHO_CLARO}Opção inválida. Por favor, tente novamente.{RESET}")
                        time.sleep(2)

            case 2:  # --> MENU DE CONSULTAS E RELATÓRIOS
                opc = consultas_e_relatorios()

                match opc:
                    case 1:
                        fluxo_listar_gastos()

                    case 2:
                        fluxo_filtrar_gasto_por_id()

                    case 3:
                        fluxo_filtrar_gastos_por_categoria()

                    case 4:
                        fluxo_filtrar_gastos_por_data()

                    case 5:
                        fluxo_filtrar_gastos_por_valor()

                    case 6:
                        fluxo_exportacao()

                    case 0:
                        continue

                    case _:
                        print(f"{VERMELHO_CLARO}Opção inválida. Por favor, tente novamente.{RESET}")
                        time.sleep(2)

            case 0:
                encerrar_programa()

            case _:
                exibir_mensagem_opcao_invalida()

if __name__ == "__main__":
    main()