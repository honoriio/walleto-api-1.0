from src.core.database import get_connection
from decimal import Decimal
from src.models.gastos import Gasto


def inserir_gasto_repository(gasto: Gasto) -> Gasto:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO gastos (nome, valor, categoria, descricao, data)
            VALUES (?, ?, ?, ?, ?)
            """,
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
    query = "SELECT * FROM gastos WHERE 1=1"
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
    for tupla in resultados:
        gastos_objetos.append(
            Gasto(
                id=tupla[0],
                nome=tupla[1],
                valor=Decimal(str(tupla[2])),
                categoria=tupla[3],
                descricao=tupla[4],
                data=tupla[5],
            )
        )

    return gastos_objetos


def consultar_gasto_por_id_repository(id: int):
    """Busca um gasto no banco e retorna um objeto Gasto ou None."""
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE id = ?", (id,))
        resultado = cursor.fetchone()

        if not resultado:
            return None

        return Gasto(
            id=resultado[0],
            nome=resultado[1],
            valor=resultado[2],
            categoria=resultado[3],
            descricao=resultado[4],
            data=resultado[5],
        )
    


def editar_gastos_repository(gasto: Gasto) -> Gasto:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE gastos
            SET nome = ?, valor = ?, categoria = ?, descricao = ?, data = ?
            WHERE id = ?
            """,
            (
                gasto.nome,
                str(gasto.valor),
                gasto.categoria,
                gasto.descricao,
                gasto.data,
                gasto.id,
            ),
        )

        conn.commit()

    return gasto


def excluir_gastos_repository(id): # exclui o gasto com base no ID informado pelo usuario
    with get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))
        conn.commit()

        return cursor.rowcount > 0 
