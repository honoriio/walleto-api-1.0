from src.controllers.gasto_controller import adicionar_gastos_controller, buscar_gasto_para_edicao_controller, editar_gastos_controller, buscar_gasto_para_exclusao_controller, excluir_gasto_controller, filtrar_gastos_nome_controller, listar_gastos_controller, exportar_gastos_controller, abrir_dashboard_controller, filtrar_gasto_por_id_controller, filtrar_gastos_por_categoria_controller, filtrar_gastos_por_data_controller, filtrar_gastos_por_valor_controller, exportar_todos_gastos_controller, abrir_dashboard_completo_controller, exportar_todos_gastos_pdf_controller
from src.views.gastos_views import coletar_dados_edicao, entrada_gastos, solicitar_id_gasto
from src.views.menus import menu_adicionar_gastos, menu_editar_gasto, menu_anterior, cabecalho_excluir_gasto, confirmar_exclusao, menu_listar_gastos, menu_filtro_exportação, cabecalho_buscar_por_id, menu_filtrar_gasto_categoria, menu_filtrar_data, menu_filtrar_valor, menu_exportacao
from src.views.tela import exibir_mensagem, mostrar_gasto, exibir_gastos, exibir_total
import time
from src.core.constants import VERDE_CLARO, VERMELHO_CLARO, AMARELO_CLARO



def fluxo_adicionar_gasto():
    menu_adicionar_gastos()
    novo_gasto = entrada_gastos()
    resultado = adicionar_gastos_controller(novo_gasto)
    if resultado["status"] == "sucesso":
        exibir_mensagem(resultado["mensagem"], VERDE_CLARO)
    else:
        exibir_mensagem(resultado["mensagem"], VERMELHO_CLARO)



def fluxo_editar_gasto():
    menu_editar_gasto()

    id_gasto = solicitar_id_gasto()
    resultado = buscar_gasto_para_edicao_controller(id_gasto)

    if resultado["status"] == "erro":
        exibir_mensagem(resultado["mensagem"], VERMELHO_CLARO)
        return

    gasto = resultado["gasto"]
    dados = coletar_dados_edicao(gasto)

    resultado_edicao = editar_gastos_controller(dados)

    if resultado_edicao["status"] == "sucesso":
        exibir_mensagem(resultado_edicao["mensagem"], VERDE_CLARO)
    else:
        exibir_mensagem(resultado_edicao["mensagem"], VERMELHO_CLARO)


def fluxo_excluir_gasto():
    id_gasto = cabecalho_excluir_gasto()

    resultado_busca = buscar_gasto_para_exclusao_controller(id_gasto)

    if resultado_busca["status"] == "erro":
        exibir_mensagem(resultado_busca["mensagem"], VERMELHO_CLARO)
        return

    mostrar_gasto(resultado_busca["gasto"])

    opc = confirmar_exclusao()

    match opc:
        case 1:
            resultado_exclusao = excluir_gasto_controller(id_gasto)

            if resultado_exclusao["status"] == "sucesso":
                exibir_mensagem(resultado_exclusao["mensagem"], VERDE_CLARO)
            else:
                exibir_mensagem(resultado_exclusao["mensagem"], VERMELHO_CLARO)

        case 2:
            exibir_mensagem("Exclusão cancelada.", AMARELO_CLARO)
            return
            

def fluxo_listar_gastos():
    menu_listar_gastos()

    resultado = listar_gastos_controller()
    gastos = resultado["gastos"]
    total = resultado["total"]

    exibir_gastos(gastos)
    exibir_total(total)

    opc = menu_filtro_exportação()

    match opc:
        case 1:
            exportar_gastos_controller(gastos)

        case 2:
            abrir_dashboard_controller(gastos)

        case 0:
            return


def fluxo_filtrar_gasto_por_id():
    id_busca = cabecalho_buscar_por_id()

    resultado = filtrar_gasto_por_id_controller(id_busca)

    if resultado["status"] == "erro":
        exibir_mensagem(resultado["mensagem"], VERMELHO_CLARO)
        return

    mostrar_gasto(resultado["gasto"])

    menu_anterior()


def fluxo_filtrar_gastos_por_categoria():
    categoria_busca = menu_filtrar_gasto_categoria()

    resultado = filtrar_gastos_por_categoria_controller(categoria_busca)
    gastos = resultado["gastos"]
    total = resultado["total"]

    exibir_gastos(gastos)
    exibir_total(total)

    opc = menu_filtro_exportação()

    match opc:
        case 1:
            exportar_gastos_controller(gastos)

        case 2:
            abrir_dashboard_controller(gastos)

        case 0:
            return
        

def fluxo_filtrar_gastos_por_data():
    data_inicio, data_final = menu_filtrar_data()

    resultado = filtrar_gastos_por_data_controller(data_inicio, data_final)
    gastos = resultado["gastos"]
    total = resultado["total"]

    exibir_gastos(gastos)
    exibir_total(total)

    opc = menu_filtro_exportação()

    match opc:
        case 1:
            exportar_gastos_controller(gastos)

        case 2:
            abrir_dashboard_controller(gastos)

        case 0:
            return
        

def fluxo_filtrar_gastos_por_valor():
    valor_min, valor_max = menu_filtrar_valor()

    resultado = filtrar_gastos_por_valor_controller(valor_min, valor_max)
    gastos = resultado["gastos"]
    total = resultado["total"]

    exibir_gastos(gastos)
    exibir_total(total)

    opc = menu_filtro_exportação()

    match opc:
        case 1:
            exportar_gastos_controller(gastos)

        case 2:
            abrir_dashboard_controller(gastos)

        case 0:
            return
        

def fluxo_exportacao():
    opc = menu_exportacao()

    match opc:
        case 1:
            resultado = exportar_todos_gastos_controller()

            exibir_mensagem(
                f"Exportado para {resultado['arquivo']}",
                VERDE_CLARO
            )
            time.sleep(2)

        case 2:
            abrir_dashboard_completo_controller()

        case 3:
            resultado = exportar_todos_gastos_pdf_controller()
            exibir_mensagem(
            f"PDF gerado com sucesso em: {resultado}",
            VERDE_CLARO
            )
            time.sleep(2)

        case 0:
            return

        case _:
            exibir_mensagem("Opção inválida. Tente novamente.", VERMELHO_CLARO)
            time.sleep(2)


def fluxo_filtrar_por_nome():
    nome = input("Digite o nome: ")
    resultado = filtrar_gastos_nome_controller(nome)

    exibir_gastos(resultado["gastos"])

