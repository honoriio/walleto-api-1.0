from src.services.gasto_service import consultar_gastos_service
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.infrastructure.exporters.pdf_exporter import exportar_gastos_pdf


def exportar_gastos_xlsx_service(
    usuario_id: int,
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    resultado = consultar_gastos_service(
        usuario_id=usuario_id,
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

    return exportar_gastos_excel(gastos)


def exportar_gastos_pdf_services(
    usuario_id: int,
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    resultado = consultar_gastos_service(
        usuario_id=usuario_id,
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

    return exportar_gastos_pdf(gastos)

