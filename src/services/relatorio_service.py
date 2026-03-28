from decimal import Decimal, ROUND_HALF_UP
from src.models.gastos import Gasto
from src.repositories.gasto_repository import consultar_gastos_repository
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.infrastructure.exporters.pdf_exporter import exportar_gastos_pdf


def calcular_gastos_services(lista_de_gastos: list[Gasto]):
    """Recebe uma lista de objetos Gasto e calcula o total."""
    if not lista_de_gastos:
        total = Decimal("0.00")
    else:
        total = sum(
            Decimal(str(gasto.valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            for gasto in lista_de_gastos
        )

    return total



def exportar_gastos_xlsx_service()-> str:
    gastos = consultar_gastos_repository()

    if not gastos:
        raise ValueError("Não há gastos para exportação.")

    caminho_arquivo = exportar_gastos_excel(gastos)

    return caminho_arquivo



def exportar_gastos_pdf_services()-> str:
    gastos = consultar_gastos_repository()

    if not gastos:
        raise ValueError("Não há gastos para exportação.")
    
    caminho_arquivo = exportar_gastos_pdf(gastos)

    return caminho_arquivo