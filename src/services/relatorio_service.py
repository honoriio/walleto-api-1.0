from src.services.gasto_service import consultar_gastos_service
from src.repositories.gasto_repository import consultar_gastos_repository
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.infrastructure.exporters.pdf_exporter import exportar_gastos_pdf


def exportar_gastos_xlsx_service(
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    resultado = consultar_gastos_service(
        nome=nome,
        categoria=categoria,
        valor_min=valor_min,
        valor_max=valor_max,
        descricao=descricao,
        data_inicio=data_inicio,
        data_final=data_final,
    )

    gastos = resultado["gastos"]

    if not gastos:
        raise ValueError("Não há gastos para exportação.")

    caminho_arquivo = exportar_gastos_excel(gastos)

    return {
        "arquivo": str(caminho_arquivo)
    }



def exportar_gastos_pdf_services(
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    resultado = consultar_gastos_service(
        nome=nome,
        categoria=categoria,
        valor_min=valor_min,
        valor_max=valor_max,
        descricao=descricao,
        data_inicio=data_inicio,
        data_final=data_final,
    )

    gastos = resultado["gastos"]

    if not gastos:
        raise ValueError("Não há gastos para exportação.")

    caminho_arquivo = exportar_gastos_pdf(gastos)

    return {
        "arquivo": str(caminho_arquivo)
    }
