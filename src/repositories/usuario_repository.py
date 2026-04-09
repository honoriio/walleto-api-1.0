from src.core.database import get_connection
from src.models.usuario import Usuario
from src.models.usuario_auth import UsuarioAuth


def inserir_usuario_repository(usuario: Usuario) -> Usuario:
    query = """
        INSERT INTO usuarios (nome, email, data_nascimento, sexo, senha_hash)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    usuario.nome,
                    usuario.email,
                    usuario.data_nascimento,
                    usuario.sexo,
                    usuario.senha_hash,
                ),
            )

            resultado = cursor.fetchone()
            conn.commit()

            usuario.id = resultado["id"]

    return usuario


def consultar_usuario_por_id_repository(usuario_id: int):
    query = """
        SELECT id, nome, email, data_nascimento, sexo
        FROM usuarios
        WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario_id,))
            resultado = cursor.fetchone()

    if resultado is None:
        return None

    return Usuario(
        id=resultado["id"],
        nome=resultado["nome"],
        email=resultado["email"],
        data_nascimento=resultado["data_nascimento"],
        sexo=resultado["sexo"],
    )

def desativar_usuario_repository(usuario_id: int) -> bool:
    query = """
        UPDATE usuarios
        SET is_active = FALSE
        WHERE id = %s AND is_active = TRUE
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario_id,))
            conn.commit()

            return cursor.rowcount > 0
    

# Esta função exclui o usuario, e a mesma esta com cascade on, isso faz com que, ao excluir um usuario, os seus gastos são excluidos juntos.
def excluir_usuario_repository(usuario_id: int) -> bool:
    query = "DELETE FROM usuarios WHERE id = %s"

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario_id,))
            conn.commit()

        return cursor.rowcount > 0
    

#Consulta usuarios por id, porem, somente usuarios ativados.
def consultar_usuario_por_email_repository(email: str) -> UsuarioAuth | None:
    query = """
        SELECT id, email, senha_hash 
        FROM usuarios 
        WHERE email = %s AND is_active = TRUE
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()

    if resultado is None:
        return None
    
    return UsuarioAuth(
        id=resultado["id"],
        email=resultado["email"],
        senha_hash=resultado["senha_hash"],
    )

    
def editar_usuario_repository(usuario: Usuario) -> Usuario | None:
    query = """
        UPDATE usuarios 
        SET nome = %s, email = %s, sexo = %s, data_nascimento = %s
        WHERE id = %s AND is_active = TRUE
    """

    params = (
        usuario.nome,
        usuario.email,
        usuario.sexo,
        usuario.data_nascimento,
        usuario.id,
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount == 0:
                return None

    return usuario