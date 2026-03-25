from src.models.gastos import Gasto
from src.services.validators.gasto_validator import validar_nome_gasto, validar_valor_gasto, validar_categoria_gasto, validar_descricao_gasto, valdiar_data_gasto

def criar_gasto(dados) -> Gasto:
    nome = validar_nome_gasto(dados.get("nome"))
    valor = validar_valor_gasto(dados.get("valor"))
    categoria = validar_categoria_gasto(dados.get("categoria"))
    descricao = validar_descricao_gasto(dados.get("descricao"))
    data = valdiar_data_gasto(dados.get("data"))

    return Gasto(nome, valor, categoria, descricao, data)

