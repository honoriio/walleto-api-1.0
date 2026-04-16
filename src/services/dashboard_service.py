from typing import List, Dict
from src.services.gasto_service import consultar_gastos_service


def obter_gastos_dashboard(usuario_id: int) -> List[Dict]:
    resultado = consultar_gastos_service(usuario_id=usuario_id)
    gastos = resultado.get("gastos", [])

    if not gastos:
        return []

    return gastos