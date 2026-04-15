import os
import sys

# garante que o root do projeto seja importável
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from streamlit.runtime.scriptrunner import main

if __name__ == "__main__":
    os.system(
        "streamlit run src/infrastructure/dashboard/streamlit_dashboard.py "
        "--server.address=0.0.0.0 "
        f"--server.port={os.getenv('PORT', 10000)}"
    )