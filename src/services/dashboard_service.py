from src.infrastructure.dashboard.streamlit_dashboard import iniciar_dashboard
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.repositories.gasto_repository import consultar_gastos_repository


def iniciar_dashboard_com_exportacao() -> dict:
    gastos = consultar_gastos_repository()

    if not gastos:
        raise ValueError("Não há gastos para gerar o dashboard.")

    caminho_arquivo = exportar_gastos_excel(gastos)

    return iniciar_dashboard(caminho_arquivo=caminho_arquivo)
