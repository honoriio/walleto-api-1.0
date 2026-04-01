import sqlite3
from src.core.config import DB_PATH

def get_connection(): # -> Função alterada para usar ROW
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def inicializar_banco():
    criar_tabela_gastos()
    criar_tabela_usuarios()


def criar_tabela_gastos():
    query = """
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                valor NUMERIC NOT NULL,
                categoria TEXT,
                descricao TEXT,
                data TEXT
            )
        """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()


def criar_tabela_usuarios():
    query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                data_nascimento TEXT NOT NULL,
                sexo TEXT NOT NULL,
                senha_hash TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP        
            )
        """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()