from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# ========================
# AUTENTICAÇÃO
# ========================

if not SECRET_KEY:
    raise ValueError("SECRET_KEY não configurada no ambiente.")

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
