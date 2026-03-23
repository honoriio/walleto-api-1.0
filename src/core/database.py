# Importações principais
from pathlib import Path
import sqlite3

# Cria e retorna a conexão com o banco de dados SQLite
def get_connection():
    # Pasta do usuário (funciona em Linux, Windows e macOS)
    app_dir = Path.home() / ".walleto"
    app_dir.mkdir(parents=True, exist_ok=True)

    db_path = app_dir / "walleto.db"

    return sqlite3.connect(db_path)




def inicializar_banco():
    criar_tabela_gastos()


def criar_tabela_gastos():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                valor NUMERIC NOT NULL,
                categoria TEXT,
                descricao TEXT,
                data TEXT
            )
        """)

        conn.commit()