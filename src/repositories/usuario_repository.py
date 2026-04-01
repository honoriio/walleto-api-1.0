from src.core.database import get_connection
from src.models.usuario import Usuario


def inserir_usuario_repository(usuario: Usuario)-> Usuario:
    query = """
        INSERT INTO usuarios (nome, email, data_nascimento, sexo, senha_hash)
        VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query,
            (
                usuario.nome,
                usuario.email,
                usuario.data_nascimento,
                usuario.sexo,
                usuario.senha_hash,
            ),
        )

        conn.commit()
        usuario.id = cursor.lastrowid

    return usuario



def consultar_usuarios_repository(
    nome=None,
    email=None,
    data_nascimento=None,
    data_inicio=None,
    data_final=None,
    sexo=None,
):
    query = """
        SELECT id, nome, email, data_nascimento, sexo
        FROM usuarios
        WHERE 1=1
    """
    params = []

    if nome:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")

    if email:
        query += " AND email = ?"
        params.append(email)

    if data_nascimento:
        query += " AND data_nascimento = ?"
        params.append(data_nascimento)

    if data_inicio:
        query += " AND data_nascimento >= ?"
        params.append(data_inicio)

    if data_final:
        query += " AND data_nascimento <= ?"
        params.append(data_final)

    if sexo:
        query += " AND sexo = ?"
        params.append(sexo)

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()

    usuarios = []

    for row in resultados:
        usuarios.append(
            Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],

        ))

    return usuarios


def consultar_usuario_por_id_repository(id: int):
    query = """
            SELECT id, nome, email, data_nascimento, sexo
            FROM usuarios
            WHERE id = ?
        """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()

    if not resultado:
        return None

    return Usuario(
        id=resultado["id"],
        nome=resultado["nome"],
        email=resultado["email"],
        data_nascimento=resultado["data_nascimento"],
        sexo=resultado["sexo"],
    )


def excluir_usuario_repository(id):
    query = "DELETE FROM usuarios WHERE id = ?"
    with get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()

        return cursor.rowcount > 0 