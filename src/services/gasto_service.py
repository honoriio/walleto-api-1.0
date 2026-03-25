from src.models.gastos import Gasto
from datetime import date
from src.utils.date_utils import formatar_data_ISO
from src.repositories.gasto_repository import inserir_gasto_repository
from src.validators.gasto_validator import validar_nome_gasto, validar_valor_gasto, validar_categoria_gasto, validar_descricao_gasto, validar_data_gasto

def criar_gasto_service(dados) -> Gasto:
    nome = validar_nome_gasto(dados.nome)
    valor = validar_valor_gasto(dados.valor)
    categoria = validar_categoria_gasto(dados.categoria)
    descricao = validar_descricao_gasto(dados.descricao)

    data_obj = dados.data if dados.data else date.today()
    data_iso = formatar_data_ISO(data_obj)

    novo_gasto = Gasto(
        nome=nome,
        valor=valor,
        categoria=categoria,
        descricao=descricao,
        data=data_iso,
    )

    gasto_criado = inserir_gasto_repository(novo_gasto)
    return gasto_criado


