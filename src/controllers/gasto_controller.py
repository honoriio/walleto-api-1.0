from src.repositories.gasto_repository import filtrar_gastos_nome_repository, inserir_gasto_repository, editar_gastos_repository, buscar_gasto_por_id_repository, excluir_gastos_repository, listar_gastos_repository, filtrar_gastos_categoria_repository, filtrar_gastos_data_repository, filtrar_gasto_valor_repository
from src.services.relatorio_service import calcular_gastos_services
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.views.fluxo_dashboard_view import painel_dashboard_em_execucao
from src.infrastructure.exporters.pdf_exporter import exportar_gastos_pdf

def adicionar_gastos_controller(novo_gasto):
    resultado = inserir_gasto_repository(novo_gasto)
    return resultado



def editar_gastos_controller(dados):
    resultado = editar_gastos_repository(dados)
    return resultado


def buscar_gasto_para_exclusao_controller(id_gasto: int):
    gasto = buscar_gasto_por_id_repository(id_gasto)

    if gasto is None:
        return {
            "status": "erro",
            "mensagem": "Gasto não encontrado.",
            "gasto": None,
        }

    return {
        "status": "sucesso",
        "mensagem": "Gasto encontrado.",
        "gasto": gasto,
    }


def excluir_gasto_controller(id_gasto: int):
    return excluir_gastos_repository(id_gasto)


def listar_gastos_controller():
    gastos = listar_gastos_repository()
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
    }


def exportar_gastos_controller(gastos):
    return exportar_gastos_excel(gastos)


def abrir_dashboard_controller(gastos):
    caminho_arquivo = exportar_gastos_excel(gastos)
    painel_dashboard_em_execucao(caminho_arquivo)
    return caminho_arquivo


def filtrar_gasto_por_id_controller(id_busca: int):
    gasto = buscar_gasto_por_id_repository(id_busca)

    if gasto is None:
        return {
            "status": "erro",
            "mensagem": "Gasto não encontrado.",
            "gasto": None,
        }

    return {
        "status": "sucesso",
        "gasto": gasto,
    }


def filtrar_gastos_por_categoria_controller(categoria):
    gastos = filtrar_gastos_categoria_repository(categoria)

    if gastos is None:
        return {
            "status": "erro",
            "mensagem": "Erro ao buscar gastos por categoria.",
            "gastos": [],
            "total": 0,
        }

    total = calcular_gastos_services(gastos)

    return {
        "status": "sucesso",
        "mensagem": "Consulta realizada com sucesso.",
        "gastos": gastos,
        "total": total,
    }


def filtrar_gastos_por_data_controller(data_inicio, data_final):
    gastos = filtrar_gastos_data_repository(data_inicio, data_final)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
    }


def filtrar_gastos_por_valor_controller(valor_min, valor_max):
    gastos = filtrar_gasto_valor_repository(valor_min, valor_max)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
    }


def exportar_todos_gastos_controller():
    gastos = listar_gastos_repository()
    arquivo = exportar_gastos_excel(gastos)

    return {
        "status": "sucesso",
        "arquivo": arquivo,
    }


def abrir_dashboard_completo_controller():
    gastos = listar_gastos_repository()
    caminho_arquivo = exportar_gastos_excel(gastos)
    painel_dashboard_em_execucao(caminho_arquivo)

    return caminho_arquivo


def buscar_gasto_para_edicao_controller(id_gasto: int):
    gasto = buscar_gasto_por_id_repository(id_gasto)

    if gasto is None:
        return {
            "status": "erro",
            "mensagem": f"Nenhum gasto encontrado com o ID {id_gasto}.",
            "gasto": None,
        }

    return {
        "status": "sucesso",
        "gasto": gasto,
    }


def filtrar_gastos_nome_controller(nome):
    gastos = filtrar_gastos_nome_repository(nome)
    return {"gastos": gastos}

def exportar_todos_gastos_pdf_controller():
    gastos = listar_gastos_repository()
    arquivo = exportar_gastos_pdf(gastos)

    return {
        "status": "sucesso",
        "arquivo": arquivo,
    }