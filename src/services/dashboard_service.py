from pathlib import Path

from src.infrastructure.dashboard.streamlit_dashboard import iniciar_dashboard
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel


def iniciar_dashboard_com_exportacao() -> dict:
    caminho_arquivo = exportar_gastos_excel()
    return iniciar_dashboard(caminho_arquivo=caminho_arquivo)

