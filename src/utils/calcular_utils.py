from decimal import ROUND_HALF_UP, Decimal
from src.models.gastos import Gasto


def calcular_gastos_utils(lista_de_gastos: list[Gasto]):
    """Recebe uma lista de objetos Gasto e calcula o total."""
    if not lista_de_gastos:
        total = Decimal("0.00")
    else:
        total = sum(
            Decimal(str(gasto.valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            for gasto in lista_de_gastos
        )

    return total

