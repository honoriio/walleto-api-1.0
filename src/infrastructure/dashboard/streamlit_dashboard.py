from __future__ import annotations

import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

from src.core.config import (
    HOST_PADRAO,
    PORTA_PADRAO,
    TIMEOUT_STREAMLIT,
    NOME_PLANILHA,
    ARQUIVO_CONTROLE_DASHBOARD,
    BASE_DIR,
)

import pandas as pd
import streamlit as st


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
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Categoria"] = df["Categoria"].fillna("Sem categoria")
    df["Descrição"] = df["Descrição"].fillna("")

    df = df.dropna(subset=["Valor", "Data"])
    return df


def renderizar_dashboard(caminho_arquivo: str | Path | None = None) -> None:
    st.set_page_config(page_title="Walleto Dashboard", layout="wide")
    st.title("Dashboard Financeiro - Walleto")

    if caminho_arquivo is None:
        caminho_arquivo = ler_caminho_arquivo_dashboard()

    if caminho_arquivo is None:
        st.info("Nenhum arquivo XLSX foi informado.")
        st.info("Abra o dashboard a partir do Walleto.")
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


def encerrar_streamlit_existente() -> None:
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True, text=True)
    time.sleep(1.5)


def abrir_dashboard(
    caminho_arquivo: str | Path,
    caminho_script: str | Path | None = None,
    porta: int = PORTA_PADRAO,
    abrir_navegador: bool = True,
) -> tuple[subprocess.Popen, str]:
    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()
    caminho_script_resolvido = obter_caminho_script_dashboard(caminho_script)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo XLSX não encontrado: {caminho_arquivo}")

    if not caminho_script_resolvido.exists():
        raise FileNotFoundError(
            f"Script do dashboard não encontrado: {caminho_script_resolvido}"
        )

    arquivo_controle = salvar_caminho_arquivo_dashboard(caminho_arquivo)
    print(f"\nArquivo de controle atualizado: {arquivo_controle}")
    print(f"Conteúdo salvo no controle: {caminho_arquivo}")

    if porta_esta_ativa(HOST_PADRAO, porta):
        print("\nDashboard já estava em execução. Reiniciando com a nova base...")
        encerrar_streamlit_existente()

    url = f"http://localhost:{porta}"
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
        processo.terminate()
        arquivo_log.close()
        raise RuntimeError(
            "O dashboard não iniciou a tempo. "
            f"Consulte o log em: {caminho_log}"
        )

    if abrir_navegador:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    return processo, url


def encerrar_processo(processo: subprocess.Popen | None) -> None:
    if processo is None:
        return

    if processo.poll() is not None:
        return

    processo.terminate()

    try:
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        processo.kill()


if __name__ == "__main__":
    renderizar_dashboard()