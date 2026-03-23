from pathlib import Path

# ========================
# BASE DO PROJETO
# ========================
BASE_DIR = Path(__file__).resolve().parents[2]

# ========================
# BANCO DE DADOS
# ========================
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "walleto.db"

# ========================
# EXPORTAÇÃO
# ========================
NOME_PLANILHA = "Gastos"

# ========================
# DASHBOARD
# ========================
HOST_PADRAO = "127.0.0.1"
PORTA_PADRAO = 8501
TIMEOUT_STREAMLIT = 15
ARQUIVO_CONTROLE_DASHBOARD = "dashboard_arquivo_atual.txt"

# ========================
# LOGS
# ========================
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ========================
# DOCUMENTOS DO USUÁRIO
# ========================
PASTA_DOCUMENTOS = Path.home() / "Documentos"
PASTA_DOCUMENTOS.mkdir(parents=True, exist_ok=True)














