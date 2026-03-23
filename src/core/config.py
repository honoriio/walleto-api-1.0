from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

# Banco de dados
DB_PATH = BASE_DIR / "data" / "walleto.db"

# Excel / exportação
NOME_PLANILHA = "Gastos"

# Dashboard
HOST_PADRAO = "127.0.0.1"
PORTA_PADRAO = 8501
TIMEOUT_STREAMLIT = 15
NOME_PLANILHA = "Gastos"
ARQUIVO_CONTROLE_DASHBOARD = "dashboard_arquivo_atual.txt"

# Logs
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Diretorio documentos
PASTA_DOCUMENTOS = Path.home() / "Documentos"