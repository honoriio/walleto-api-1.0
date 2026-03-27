from src.core.database import get_connection
from decimal import Decimal
from src.models.gastos import Gasto
from src.utils.date_utils import formatar_data_ISO


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



def excluir_gastos_repository(id): # exclui o gasto com base no ID informado pelo usuario
    with get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))
        conn.commit()

        return cursor.rowcount > 0 
                 



def buscar_gasto_por_id_repository(id: int):
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





def listar_gastos_repository():
    """Busca todos os gastos e retorna uma lista de objetos Gasto."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos")
        resultados = cursor.fetchall()
        
        gastos_objetos = []
        for tupla in resultados:
            gastos_objetos.append(
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=tupla[2],
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5]
                )
            )

        return gastos_objetos



def filtrar_gastos_data_repository(data_inicio, data_final):
    with get_connection() as conn:
        cursor = conn.cursor()

        if data_inicio is not None and data_final is not None:
            data_inicio = formatar_data_ISO(data_inicio)
            data_final = formatar_data_ISO(data_final)

            cursor.execute(
                "SELECT * FROM gastos WHERE data BETWEEN ? AND ?",
                (data_inicio, data_final)
            )

        elif data_inicio is not None:
            data_inicio = formatar_data_ISO(data_inicio)

            cursor.execute(
                "SELECT * FROM gastos WHERE data >= ?",
                (data_inicio,)
            )

        elif data_final is not None:
            data_final = formatar_data_ISO(data_final)

            cursor.execute(
                "SELECT * FROM gastos WHERE data <= ?",
                (data_final,)
            )

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
                    data=tupla[5]
                )
            )

        return gastos_objetos


def filtrar_gasto_valor_repository(valor_min, valor_max):
    with get_connection() as conn:
        cursor = conn.cursor()

        if valor_min is not None and valor_max is not None:
            cursor.execute(
                "SELECT * FROM gastos WHERE valor BETWEEN ? AND ?",
                (str(valor_min), str(valor_max))
            )

        elif valor_min is not None:
            cursor.execute(
                "SELECT * FROM gastos WHERE valor >= ?",
                (str(valor_min),)
            )

        elif valor_max is not None:
            cursor.execute(
                "SELECT * FROM gastos WHERE valor <= ?",
                (str(valor_max),)
            )

        resultados = cursor.fetchall()

        gastos_objetos = []
        for tupla in resultados:
            gastos_objetos.append(
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=tupla[2],
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5],
                )
            )

        return gastos_objetos



def filtrar_gastos_categoria_repository(categoria):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE categoria = ?", (categoria,))
        resultados = cursor.fetchall()

        return [
            Gasto(
                id=tupla[0],
                nome=tupla[1],
                valor=tupla[2],
                categoria=tupla[3],
                descricao=tupla[4],
                data=tupla[5],
            )
            for tupla in resultados
        ]



def filtrar_gastos_nome_repository(nome):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE nome = ?", (nome,))
        resultados = cursor.fetchall()

        return [
            Gasto(
                id=tupla[0],
                nome=tupla[1],
                valor=tupla[2],
                categoria=tupla[3],
                descricao=tupla[4],
                data=tupla[5],
            )
            for tupla in resultados
        ]

