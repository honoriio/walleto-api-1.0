from src.infrastructure.dashboard.streamlit_dashboard import iniciar_dashboard
from src.infrastructure.exporters.excel_exporter import exportar_gastos_excel
from src.services.gasto_service import consultar_gastos_service


def iniciar_dashboard_com_exportacao(usuario_id: int) -> dict:
    resultado = consultar_gastos_service(usuario_id=usuario_id)
    gastos = resultado["gastos"]

    if not gastos:
        raise ValueError("Não há gastos para gerar o dashboard.")

    caminho_arquivo = exportar_gastos_excel(gastos)

    return iniciar_dashboard(caminho_arquivo=caminho_arquivo)