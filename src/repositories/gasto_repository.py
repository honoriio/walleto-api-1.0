from src.core.database import get_connection
from decimal import Decimal
from src.models.gastos import Gasto


def inserir_gasto_repository(gasto: Gasto) -> Gasto:
    query = """
    INSERT INTO gastos (nome, valor, categoria, descricao, data)
    VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query,
            (
                gasto.nome,
                str(gasto.valor),
                gasto.categoria,
                gasto.descricao,
                gasto.data,
            ),
        )

        conn.commit()
        gasto.id = cursor.lastrowid

    return gasto


def consultar_gastos_repository(
    nome=None,
    categoria=None,
    valor_min=None,
    valor_max=None,
    descricao=None,
    data_inicio=None,
    data_final=None,
):
    query = "SELECT id, nome, valor, categoria, descricao, data FROM gastos WHERE 1=1"
    params = []

    if nome:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")

    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)

    if valor_min is not None:
        query += " AND valor >= ?"
        params.append(str(valor_min))

    if valor_max is not None:
        query += " AND valor <= ?"
        params.append(str(valor_max))

    if descricao is not None and descricao:
        query += " AND descricao LIKE ?"
        params.append(f"%{descricao}%")

    if data_inicio:
        query += " AND data >= ?"
        params.append(data_inicio)

    if data_final:
        query += " AND data <= ?"
        params.append(data_final)

    query += " ORDER BY data DESC, id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()

    gastos_objetos = []
    for row in resultados:
        gastos_objetos.append(
            Gasto(
                id=row["id"],
                nome=row["nome"],
                valor=Decimal(str(row["valor"])),
                categoria=row["categoria"],
                descricao=row["descricao"],
                data=row["data"],
            )
        )

    return gastos_objetos


def consultar_gasto_por_id_repository(id: int):
    """Busca um gasto no banco e retorna um objeto Gasto ou None."""

    query = """
    SELECT id, nome, valor, categoria, descricao, data
    FROM gastos
    WHERE id = ?
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()

    if resultado is None:
        return None

    return Gasto(
        id=resultado["id"],
        nome=resultado["nome"],
        valor=Decimal(str(resultado["valor"])),
        categoria=resultado["categoria"],
        descricao=resultado["descricao"],
        data=resultado["data"],
    )


def editar_gastos_repository(gasto: Gasto) -> Gasto:
    query = """
    UPDATE gastos
    SET nome = ?, valor = ?, categoria = ?, descricao = ?, data = ?
    WHERE id = ?
    """

    params = (
        gasto.nome,
        str(gasto.valor),
        gasto.categoria,
        gasto.descricao,
        gasto.data,
        gasto.id,
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    return gasto


def excluir_gastos_repository(id): # exclui o gasto com base no ID informado pelo usuario
    with get_connection() as conn: 
        query = """
        DELETE FROM gastos WHERE id = ?
        """
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()

        return cursor.rowcount > 0 
