import logging
from src.core.database import get_connection
from decimal import Decimal
from src.models.gastos import Gasto

logger = logging.getLogger(__name__)

# Ja refatorada para Postgres com suporte a decimal
def inserir_gasto_repository(gasto: Gasto) -> Gasto:
    query = """
    INSERT INTO gastos (nome, valor, categoria, descricao, data, usuario_id)
    VALUES (%s,%s,%s,%s,%s,%s)
    RETURNING id
    """

    params = (
        gasto.nome,
        gasto.valor,
        gasto.categoria,
        gasto.descricao,
        gasto.data,
        gasto.usuario_id
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            resultado = cursor.fetchone()
            conn.commit()
            gasto.id = resultado["id"]

    return gasto


# Função ja refatorada para Postgres, adicionada recurso para usar decimal
def consultar_gastos_repository(
    usuario_id: int,
    nome: str | None = None,
    categoria: str | None = None,
    valor_min: Decimal | None = None,
    valor_max: Decimal | None = None,
    descricao: str | None = None,
    data_inicio: str | None = None,
    data_final: str | None = None,
    ) -> list[Gasto]:
    query = """
        SELECT id, nome, valor, categoria, descricao, data, usuario_id
        FROM gastos
        WHERE usuario_id = %s
    """
    params = [usuario_id]

    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")

    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)

    if valor_min is not None:
        query += " AND valor >= %s"
        params.append(valor_min)

    if valor_max is not None:
        query += " AND valor <= %s"
        params.append(valor_max)

    if descricao:
        query += " AND descricao ILIKE %s"
        params.append(f"%{descricao}%")

    if data_inicio:
        query += " AND data >= %s"
        params.append(data_inicio)

    if data_final:
        query += " AND data <= %s"
        params.append(data_final)

    query += " ORDER BY data DESC, id DESC"

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()

    gastos_objetos = [
        Gasto(
            id=row["id"],
            nome=row["nome"],
            valor=row["valor"],
            categoria=row["categoria"],
            descricao=row["descricao"],
            data=row["data"],
            usuario_id=row["usuario_id"],
        )
        for row in resultados
    ]

    return gastos_objetos


def consultar_gasto_por_id_repository(gasto_id: int, usuario_id: int) -> Gasto | None:
    query = """
    SELECT id, nome, valor, categoria, descricao, data, usuario_id
    FROM gastos
    WHERE id = %s AND usuario_id = %s
    """
    params = (gasto_id, usuario_id)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            resultado = cursor.fetchone()

    if resultado is None:
        return None

    
    return Gasto(
        id=resultado["id"],
        nome=resultado["nome"],
        valor=resultado["valor"],
        categoria=resultado["categoria"],
        descricao=resultado["descricao"],
        data=resultado["data"],
        usuario_id=resultado["usuario_id"],
    )


def editar_gasto_repository(gasto: Gasto) -> Gasto | None:
    query = """
        UPDATE gastos
        SET nome = %s, valor = %s, categoria = %s, descricao = %s, data = %s
        WHERE id = %s AND usuario_id = %s
    """

    params = (
        gasto.nome,
        gasto.valor,
        gasto.categoria,
        gasto.descricao,
        gasto.data,
        gasto.id,
        gasto.usuario_id,
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount == 0:
                return None

    return gasto


def excluir_gasto_repository(gasto_id: int, usuario_id: int) -> bool:
    query = """
        DELETE FROM gastos
        WHERE id = %s AND usuario_id = %s
    """
    params = (gasto_id, usuario_id)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()

            return cursor.rowcount > 0

