import psycopg2
from psycopg2.extras import RealDictCursor
from src.core.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )


def criar_tabela_usuarios(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        data_nascimento DATE NOT NULL,
        sexo VARCHAR(20) NOT NULL,
        senha_hash TEXT NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)


def criar_tabela_gastos(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            valor NUMERIC(10,2) NOT NULL,
            categoria VARCHAR(100),
            descricao TEXT,
            data DATE NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id)
                REFERENCES usuarios(id)
                ON DELETE CASCADE
        );
    """)

def inicializar_banco():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            criar_tabela_usuarios(cursor)
            criar_tabela_gastos(cursor)
        conn.commit()
