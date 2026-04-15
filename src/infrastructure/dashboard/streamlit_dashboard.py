from __future__ import annotations

import os
import requests
import streamlit as st

import json
import os
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import pandas as pd
import streamlit as st

from src.core.config import (
    ARQUIVO_CONTROLE_DASHBOARD,
    BASE_DIR,
    HOST_PADRAO,
    NOME_PLANILHA,
    PORTA_PADRAO,
    TIMEOUT_STREAMLIT,
)

ARQUIVO_ESTADO_DASHBOARD = "dashboard_runtime.json"


def formatar_moeda_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def obter_diretorio_base() -> Path:
    return BASE_DIR


def obter_pasta_logs() -> Path:
    pasta_logs = obter_diretorio_base() / "logs"
    pasta_logs.mkdir(parents=True, exist_ok=True)
    return pasta_logs


def obter_arquivo_log_dashboard() -> Path:
    return obter_pasta_logs() / "streamlit_dashboard.log"


def obter_arquivo_controle_dashboard() -> Path:
    return obter_pasta_logs() / ARQUIVO_CONTROLE_DASHBOARD


def obter_arquivo_estado_dashboard() -> Path:
    return obter_pasta_logs() / ARQUIVO_ESTADO_DASHBOARD


def salvar_caminho_arquivo_dashboard(caminho_arquivo: str | Path) -> Path:
    caminho = Path(caminho_arquivo).expanduser().resolve()
    arquivo_controle = obter_arquivo_controle_dashboard()
    arquivo_controle.write_text(str(caminho), encoding="utf-8")
    return arquivo_controle


def ler_caminho_arquivo_dashboard() -> Path | None:
    arquivo_controle = obter_arquivo_controle_dashboard()

    if not arquivo_controle.exists():
        return None

    conteudo = arquivo_controle.read_text(encoding="utf-8").strip()
    if not conteudo:
        return None

    return Path(conteudo).expanduser().resolve()


def salvar_estado_dashboard(estado: dict) -> Path:
    arquivo_estado = obter_arquivo_estado_dashboard()
    arquivo_estado.write_text(
        json.dumps(estado, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return arquivo_estado


def ler_estado_dashboard() -> dict | None:
    arquivo_estado = obter_arquivo_estado_dashboard()

    if not arquivo_estado.exists():
        return None

    try:
        conteudo = arquivo_estado.read_text(encoding="utf-8").strip()
        if not conteudo:
            return None
        return json.loads(conteudo)
    except (json.JSONDecodeError, OSError):
        return None


def limpar_estado_dashboard() -> None:
    arquivo_estado = obter_arquivo_estado_dashboard()
    if arquivo_estado.exists():
        arquivo_estado.unlink()


def validar_colunas_obrigatorias(df: pd.DataFrame) -> None:
    colunas_obrigatorias = {"Nome", "Valor", "Categoria", "Data", "Descrição"}
    colunas_encontradas = set(df.columns)

    colunas_faltando = colunas_obrigatorias - colunas_encontradas
    if colunas_faltando:
        raise ValueError(
            "O arquivo XLSX não contém todas as colunas esperadas. "
            f"Faltando: {', '.join(sorted(colunas_faltando))}"
        )


def carregar_dados_excel(caminho_arquivo: str | Path) -> pd.DataFrame:
    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo XLSX não encontrado: {caminho_arquivo}")

    df = pd.read_excel(caminho_arquivo, sheet_name=NOME_PLANILHA)

    validar_colunas_obrigatorias(df)
    
    df = df[df["Nome"] != "TOTAL"].copy()
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
    df["Categoria"] = df["Categoria"].fillna("Sem categoria")
    df["Descrição"] = df["Descrição"].fillna("")
    df = df.dropna(subset=["Valor", "Data"])

    return df


def renderizar_dashboard(caminho_arquivo: str | Path | None = None) -> None:
    token = st.query_params.get("token")

    if not token:
        st.error("Acesso não autorizado")
        st.stop()

    API_URL = os.getenv("API_URL")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{API_URL}/usuarios/me",
        headers=headers
    )

    if response.status_code != 200:
        st.error("Token inválido ou expirado")
        st.stop()

    usuario = response.json()

    st.set_page_config(page_title="Walleto Dashboard", layout="wide")
    st.title(f"Dashboard Financeiro - {usuario.get('email', '')}")

    if caminho_arquivo is None:
        caminho_arquivo = ler_caminho_arquivo_dashboard()

    if caminho_arquivo is None:
        st.info("Nenhum arquivo XLSX foi informado.")
        st.info("Inicie o dashboard pela API.")
        return

    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()

    if not caminho_arquivo.exists():
        st.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return

    try:
        df = carregar_dados_excel(caminho_arquivo)
    except Exception as erro:
        st.error(f"Erro ao carregar o arquivo Excel: {erro}")
        return

    if df.empty:
        st.warning("O arquivo foi carregado, mas não há dados para exibir.")
        return

    col_filtro1, col_filtro2 = st.columns(2)

    categorias = sorted(df["Categoria"].dropna().unique().tolist())
    categoria_selecionada = col_filtro1.multiselect(
        "Filtrar por categoria",
        options=categorias,
        default=categorias,
    )

    data_min = df["Data"].min()
    data_max = df["Data"].max()

    intervalo_datas = col_filtro2.date_input(
        "Filtrar por período",
        value=(data_min, data_max),
    )

    df_filtrado = df[df["Categoria"].isin(categoria_selecionada)].copy()

    if isinstance(intervalo_datas, tuple) and len(intervalo_datas) == 2:
        data_inicio = pd.to_datetime(intervalo_datas[0])
        data_fim = pd.to_datetime(intervalo_datas[1])

        df_filtrado = df_filtrado[
            (df_filtrado["Data"] >= data_inicio)
            & (df_filtrado["Data"] <= data_fim)
        ]

    total_gasto = df_filtrado["Valor"].sum()
    quantidade_gastos = len(df_filtrado)
    ticket_medio = df_filtrado["Valor"].mean() if quantidade_gastos > 0 else 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total gasto", formatar_moeda_brl(total_gasto))
    col2.metric("Quantidade de gastos", quantidade_gastos)
    col3.metric("Ticket médio", formatar_moeda_brl(ticket_medio))

    st.divider()

    st.subheader("Gastos por categoria")
    gastos_categoria = (
        df_filtrado.groupby("Categoria", as_index=False)["Valor"]
        .sum()
        .sort_values("Valor", ascending=False)
    )

    if not gastos_categoria.empty:
        st.bar_chart(gastos_categoria.set_index("Categoria"))
    else:
        st.info("Nenhum dado para exibir no gráfico de categorias.")

    st.subheader("Gastos por mês")
    df_filtrado["Mes"] = df_filtrado["Data"].dt.to_period("M").astype(str)

    gastos_mes = (
        df_filtrado.groupby("Mes", as_index=False)["Valor"]
        .sum()
        .sort_values("Mes")
    )

    if not gastos_mes.empty:
        st.line_chart(gastos_mes.set_index("Mes"))
    else:
        st.info("Nenhum dado para exibir no gráfico mensal.")

    st.subheader("Últimos gastos")
    df_exibicao = df_filtrado.sort_values("Data", ascending=False).copy()
    df_exibicao["Data"] = df_exibicao["Data"].dt.strftime("%d/%m/%Y")
    df_exibicao["Valor"] = df_exibicao["Valor"].apply(formatar_moeda_brl)

    st.dataframe(df_exibicao, width="stretch")


def porta_esta_ativa(host: str, porta: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, porta)) == 0


def esperar_streamlit(
    host: str = HOST_PADRAO,
    porta: int = PORTA_PADRAO,
    timeout: int = TIMEOUT_STREAMLIT,
) -> bool:
    inicio = time.time()

    while time.time() - inicio < timeout:
        if porta_esta_ativa(host, porta):
            return True
        time.sleep(0.5)

    return False


def obter_caminho_script_dashboard(caminho_script: str | Path | None = None) -> Path:
    if caminho_script is None:
        return Path(__file__).expanduser().resolve()
    return Path(caminho_script).expanduser().resolve()


def _encerrar_pid(pid: int) -> None:
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
        )
        return  

    try: # --> Somente o pylanc apagando o codigo
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)

        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            return

        os.kill(pid, signal.SIGKILL)

    except ProcessLookupError:
        return


def encerrar_dashboard_existente() -> None:
    estado = ler_estado_dashboard()

    if estado and estado.get("pid"):
        _encerrar_pid(int(estado["pid"]))
        time.sleep(1.5)

    limpar_estado_dashboard()


def iniciar_dashboard(
    caminho_arquivo: str | Path,
    caminho_script: str | Path | None = None,
    porta: int = PORTA_PADRAO,
    abrir_navegador: bool = True,
    ) -> dict:
    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()
    caminho_script_resolvido = obter_caminho_script_dashboard(caminho_script)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo XLSX não encontrado: {caminho_arquivo}")

    if not caminho_script_resolvido.exists():
        raise FileNotFoundError(
            f"Script do dashboard não encontrado: {caminho_script_resolvido}"
        )

    salvar_caminho_arquivo_dashboard(caminho_arquivo)

    if porta_esta_ativa(HOST_PADRAO, porta):
        encerrar_dashboard_existente()

    url = f"http://{HOST_PADRAO}:{porta}"
    caminho_log = obter_arquivo_log_dashboard()
    arquivo_log = open(caminho_log, "a", encoding="utf-8")

    try:
        processo = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(caminho_script_resolvido),
                "--server.address",
                HOST_PADRAO,
                "--server.port",
                str(porta),
                "--server.headless",
                "true",
            ],
            stdout=arquivo_log,
            stderr=arquivo_log,
            cwd=str(BASE_DIR),
        )
    except Exception:
        arquivo_log.close()
        raise

    pronto = esperar_streamlit(porta=porta)

    if not pronto:
        try:
            processo.terminate()
        except Exception:
            pass
        arquivo_log.close()
        raise RuntimeError(
            f"O dashboard não iniciou a tempo. Consulte o log em: {caminho_log}"
        )

    estado = {
        "pid": processo.pid,
        "url": url,
        "porta": porta,
        "host": HOST_PADRAO,
        "caminho_arquivo": str(caminho_arquivo),
        "caminho_script": str(caminho_script_resolvido),
        "log": str(caminho_log),
        "ativo": True,
    }
    salvar_estado_dashboard(estado)

    if abrir_navegador:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    return estado


def obter_status_dashboard() -> dict:
    estado = ler_estado_dashboard()

    if not estado:
        return {
            "ativo": False,
            "url": None,
            "pid": None,
            "porta": PORTA_PADRAO,
        }

    ativo = porta_esta_ativa(estado.get("host", HOST_PADRAO), int(estado.get("porta", PORTA_PADRAO)))
    estado["ativo"] = ativo
    return estado


def encerrar_dashboard() -> dict:
    estado = ler_estado_dashboard()

    if not estado:
        return {
            "mensagem": "Nenhum dashboard em execução.",
            "ativo": False,
        }

    pid = estado.get("pid")
    if pid:
        _encerrar_pid(int(pid))
        time.sleep(1)

    limpar_estado_dashboard()

    return {
        "mensagem": "Dashboard encerrado com sucesso.",
        "ativo": False,
    }


if __name__ == "__main__":
    renderizar_dashboard()