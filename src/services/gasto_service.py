from src.models.gastos import Gasto
from datetime import date
from src.utils.date_utils import formatar_data_ISO
from src.services.relatorio_service import calcular_gastos_services
from src.repositories.gasto_repository import inserir_gasto_repository, listar_gastos_repository, buscar_gasto_por_id_repository, filtrar_gastos_categoria_repository, filtrar_gastos_nome_repository
from src.validators.gasto_validator import validar_nome_gasto, validar_valor_gasto, validar_categoria_gasto, validar_descricao_gasto

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


def listar_gastos_service():
    gastos = listar_gastos_repository()
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos)
    }


def buscar_gasto_por_id_service(id):
    gasto = buscar_gasto_por_id_repository(id)
    if not gasto:
        raise ValueError("Não existe gasto com esse ID")
    
    return gasto


def buscar_gastos_por_categoria_service(categoria):
    categoria = validar_categoria_gasto(categoria)
    gastos = filtrar_gastos_categoria_repository(categoria)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos)
    }


def buscar_gastos_por_nome_service(nome):
    nome = validar_nome_gasto(nome)
    gastos = filtrar_gastos_nome_repository(nome)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos)
    }

