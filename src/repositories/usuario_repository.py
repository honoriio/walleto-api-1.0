import logging
import sqlite3

from src.core.database import get_connection
from src.models.usuario import Usuario
from src.models.usuario_auth import UsuarioAuth

logger = logging.getLogger(__name__)

def inserir_usuario_repository(usuario: Usuario) -> Usuario:
    query = """
        INSERT INTO usuarios (nome, email, data_nascimento, sexo, senha_hash)
        VALUES (?, ?, ?, ?, ?)
    """

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
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

            conn.commit()
            usuario.id = cursor.lastrowid

        return usuario

    except sqlite3.IntegrityError:
        logger.warning("Erro de integridade ao inserir usuário - email=%s", usuario.email)
        raise

    except sqlite3.Error:
        logger.exception("Erro de banco ao inserir usuário - email=%s", usuario.email)
        raise


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

    if resultado is  None:
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
    


def consultar_usuario_por_email_repository(email: str) -> UsuarioAuth | None:
    query = """
    SELECT id, email, senha_hash FROM usuarios WHERE email = ?
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        resultado = cursor.fetchone()

    if resultado is None:
        return None
    
    return UsuarioAuth(
        id=resultado["id"],
        email=resultado["email"],
        senha_hash=resultado["senha_hash"],
    )
    
def editar_usuario_repository(usuario: Usuario)-> Usuario:
    query = """
    UPDATE usuarios 
    SET nome = ?, email = ?, sexo = ?, data_nascimento = ?
    WHERE id = ?
    """

    params = (
        usuario.nome, 
        usuario.email,
        usuario.sexo,
        usuario.data_nascimento,
        usuario.id,
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    
    return usuario