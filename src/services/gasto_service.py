import logging
from datetime import date

from src.api.schemas.gasto_schema import GastoCreateRequest, GastoUpdateRequest
from src.core.exceptions import FiltroInvalidoError, NotFoundError
from src.models.gastos import Gasto
from src.repositories.gasto_repository import (
    consultar_gasto_por_id_repository,
    consultar_gastos_repository,
    editar_gasto_repository,
    excluir_gasto_repository,
    inserir_gasto_repository,
)
from src.utils.calcular_utils import calcular_gastos_utils
from src.utils.date_utils import formatar_data_ISO
from src.validators.gasto_validator import (
    validar_categoria_gasto,
    validar_data_gasto,
    validar_descricao_gasto,
    validar_id_gasto,
    validar_nome_gasto,
    validar_valor_gasto,
)
from src.validators.usuario_validator import validar_id_usuario

logger = logging.getLogger(__name__)


def criar_gastos_service(dados: GastoCreateRequest, usuario_id: int) -> Gasto:
    nome = validar_nome_gasto(dados.nome)
    valor = validar_valor_gasto(dados.valor)
    categoria = validar_categoria_gasto(dados.categoria)
    descricao = validar_descricao_gasto(dados.descricao)
    data  = dados.data if dados.data else date.today()
    data_obj = validar_data_gasto(data)
    usuario_id = validar_id_usuario(usuario_id)
    novo_gasto = Gasto(
        nome=nome,
        valor=valor,
        categoria=categoria,
        descricao=descricao,
        data=data_obj,
        usuario_id=usuario_id,
    )

    gasto_criado = inserir_gasto_repository(novo_gasto)
    return gasto_criado


def consultar_gastos_service(
    usuario_id: int,
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    if nome is not None:
        nome = validar_nome_gasto(nome)

    if categoria is not None:
        categoria = validar_categoria_gasto(categoria)

    if valor_min is not None:
        try:
            valor_min = validar_valor_gasto(valor_min)
        except ValueError:
            raise FiltroInvalidoError("Valor mínimo inválido.")

    if valor_max is not None:
        try:
            valor_max = validar_valor_gasto(valor_max)
        except ValueError:
            raise FiltroInvalidoError("Valor máximo inválido.")

    if valor_min is not None and valor_max is not None:
        if valor_min > valor_max:
            raise FiltroInvalidoError(
                "Valor mínimo não pode ser maior que valor máximo."
            )

    if descricao is not None:
        descricao = validar_descricao_gasto(descricao)

    if data_inicio is not None:
        data_inicio = validar_data_gasto(data_inicio)

    if data_final is not None:
        data_final = validar_data_gasto(data_final)

    if data_inicio is not None and data_final is not None:
        if data_inicio > data_final:
            raise FiltroInvalidoError(
                "Data inicial não pode ser maior que data final."
            )

    gastos = consultar_gastos_repository(
        usuario_id=usuario_id,
        nome=nome,
        categoria=categoria,
        valor_min=valor_min,
        valor_max=valor_max,
        descricao=descricao,
        data_inicio=data_inicio,
        data_final=data_final,
    )

    total = calcular_gastos_utils(gastos)

    return {
        "gastos": gastos,
        "total": total,
        "quantidade": len(gastos),
    }


def consultar_gastos_por_id_service(gasto_id: int, usuario_id: int) -> Gasto:
    gasto_id = validar_id_gasto(gasto_id)
    usuario_id_valido = validar_id_usuario(usuario_id)

    gasto = consultar_gasto_por_id_repository(gasto_id)

    if not gasto:
        raise NotFoundError("Gasto não encontrado.")

    if gasto.usuario_id != usuario_id_valido:
        logger.warning(
            "Acesso negado | usuario_id=%s | gasto_id=%s | dono_id=%s",
            usuario_id_valido,
            gasto_id,
            gasto.usuario_id,
        )
        raise PermissionError("Acesso negado.")

    return gasto


def editar_gastos_service(
    gasto_id: int,
    dados: GastoUpdateRequest,
    usuario_id: int,
    ) -> Gasto:
    gasto_id = validar_id_gasto(gasto_id)
    gasto_atual = consultar_gasto_por_id_repository(gasto_id, usuario_id)

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
    validar_data_gasto(dados.data)
    if dados.data is not None
    else gasto_atual.data
    )

    gasto_editado = Gasto(
        id=gasto_id,
        nome=nome_final,
        valor=valor_final,
        categoria=categoria_final,
        descricao=descricao_final,
        data=data_final,
        usuario_id=usuario_id,
    )

    return editar_gasto_repository(gasto_editado)


def excluir_gastos_service(gasto_id: int, usuario_id: int) -> None:
    gasto_id = validar_id_gasto(gasto_id)
    usuario_id = validar_id_usuario(usuario_id)
    excluido = excluir_gasto_repository(gasto_id, usuario_id)

    if not excluido:
        raise NotFoundError("Não existe gasto com esse ID.")
    
    