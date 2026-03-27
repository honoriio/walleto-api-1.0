from src.models.gastos import Gasto
from datetime import date
from src.utils.date_utils import formatar_data_ISO
from src.core.exceptions import NotFoundError
from src.services.relatorio_service import calcular_gastos_services
from src.repositories.gasto_repository import inserir_gasto_repository, listar_gastos_repository, buscar_gasto_por_id_repository, filtrar_gastos_categoria_repository, filtrar_gastos_nome_repository, filtrar_gasto_valor_repository, filtrar_gastos_data_repository, editar_gastos_repository, excluir_gastos_repository
from src.validators.gasto_validator import validar_nome_gasto, validar_valor_gasto, validar_categoria_gasto, validar_descricao_gasto, validar_data_gasto, validar_id_gasto

def criar_gastos_service(dados) -> Gasto:
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


def buscar_gastos_por_id_service(id):
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


def buscar_gastos_por_valor_service(valor_min, valor_max):
    
    if valor_min is None and valor_max is None:
        raise ValueError("Informe valor_min ou valor_max")

    if valor_min is not None:
        valor_min = validar_valor_gasto(valor_min)

    if valor_max is not None:
        valor_max = validar_valor_gasto(valor_max)

    if valor_min is not None and valor_max is not None:
        if valor_min > valor_max:
            raise ValueError("valor_min não pode ser maior que valor_max")

    gastos = filtrar_gasto_valor_repository(valor_min, valor_max)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos)
    }


def buscar_gastos_por_data_service(data_inicio, data_final):
    
    if data_inicio is None and data_final is None:
        raise ValueError("Informe data_inicio e data_final")
    
    if data_inicio is not None:
        data_inicio = validar_data_gasto(data_inicio)
        

    if data_final is not None:
        data_final = validar_data_gasto(data_final)

    if data_inicio is not None and data_final is not None:
        if data_inicio > data_final:
            raise ValueError("A data inicial não pode ser maior que a data final")
        
    gastos = filtrar_gastos_data_repository(data_inicio, data_final)
    total = calcular_gastos_services(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos)
    }
    

def editar_gastos_service(id: int, dados) -> Gasto:
    id = validar_id_gasto(id)
    gasto_atual = buscar_gasto_por_id_repository(id)

    if not gasto_atual:
        raise NotFoundError("Não existe gasto com esse ID.")

    nome_final = (
        validar_nome_gasto(dados.nome)
        if dados.nome is not None
        else gasto_atual.nome
    )

    valor_final = (
        validar_valor_gasto(dados.valor)
        if dados.valor is not None
        else gasto_atual.valor
    )

    categoria_final = (
        validar_categoria_gasto(dados.categoria)
        if dados.categoria is not None
        else gasto_atual.categoria
    )

    descricao_final = (
        validar_descricao_gasto(dados.descricao)
        if dados.descricao is not None
        else gasto_atual.descricao
    )

    data_final = (
        formatar_data_ISO(dados.data)
        if dados.data is not None
        else gasto_atual.data
    )

    gasto_editado = Gasto(
        id=id,
        nome=nome_final,
        valor=valor_final,
        categoria=categoria_final,
        descricao=descricao_final,
        data=data_final,
    )

    return editar_gastos_repository(gasto_editado)



def excluir_gastos_service(id: int) -> None:
    id = validar_id_gasto(id)


    excluido = excluir_gastos_repository(id)

    if not excluido:
        raise NotFoundError("Não existe gasto com esse ID.")