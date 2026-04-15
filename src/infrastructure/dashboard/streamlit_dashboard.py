from __future__ import annotations

import os
import requests
import streamlit as st

import json
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import pandas as pd

from src.core.config import (
    ARQUIVO_CONTROLE_DASHBOARD,
    BASE_DIR,
    HOST_PADRAO,
    NOME_PLANILHA,
    PORTA_PADRAO,
    TIMEOUT_STREAMLIT,
)

ARQUIVO_ESTADO_DASHBOARD = "dashboard_runtime.json"


# =========================
# UTILITÁRIOS
# =========================

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


# =========================
# EXCEL
# =========================

def validar_colunas_obrigatorias(df: pd.DataFrame) -> None:
    colunas_obrigatorias = {"Nome", "Valor", "Categoria", "Data", "Descrição"}
    colunas_faltando = colunas_obrigatorias - set(df.columns)

    if colunas_faltando:
        raise ValueError(
            f"Colunas faltando: {', '.join(sorted(colunas_faltando))}"
        )


def carregar_dados_excel(caminho_arquivo: str | Path) -> pd.DataFrame:
    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    df = pd.read_excel(caminho_arquivo, sheet_name=NOME_PLANILHA)

    validar_colunas_obrigatorias(df)

    df = df[df["Nome"] != "TOTAL"].copy()
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
    df["Categoria"] = df["Categoria"].fillna("Sem categoria")
    df["Descrição"] = df["Descrição"].fillna("")
    df = df.dropna(subset=["Valor", "Data"])

    return df


# =========================
# DASHBOARD STREAMLIT
# =========================

def renderizar_dashboard(caminho_arquivo: str | Path | None = None) -> None:
    token = st.query_params.get("token")

    if not token:
        st.error("Acesso não autorizado")
        st.stop()

    API_URL = os.getenv("API_URL")

    if not API_URL:
        st.error("API_URL não configurada no ambiente")
        st.stop()

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"{API_URL}/usuarios/me",
            headers=headers,
            timeout=10
        )
    except Exception:
        st.error("Falha ao conectar na API")
        st.stop()

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
        return

    caminho_arquivo = Path(caminho_arquivo).expanduser().resolve()

    if not caminho_arquivo.exists():
        st.error("Arquivo não encontrado")
        return

    df = carregar_dados_excel(caminho_arquivo)

    if df.empty:
        st.warning("Sem dados para exibir")
        return

    col1, col2 = st.columns(2)

    categorias = sorted(df["Categoria"].dropna().unique().tolist())

    categoria_selecionada = col1.multiselect(
        "Categorias",
        categorias,
        default=categorias
    )

    data_min, data_max = df["Data"].min(), df["Data"].max()

    intervalo = col2.date_input(
        "Período",
        value=(data_min, data_max)
    )

    df_filtrado = df[df["Categoria"].isin(categoria_selecionada)]

    if isinstance(intervalo, tuple):
        inicio, fim = intervalo
        df_filtrado = df_filtrado[
            (df_filtrado["Data"] >= pd.to_datetime(inicio)) &
            (df_filtrado["Data"] <= pd.to_datetime(fim))
        ]

    total = df_filtrado["Valor"].sum()
    qtd = len(df_filtrado)
    media = df_filtrado["Valor"].mean() if qtd else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", formatar_moeda_brl(total))
    c2.metric("Qtd", qtd)
    c3.metric("Média", formatar_moeda_brl(media))

    st.divider()

    st.subheader("Por categoria")
    st.bar_chart(df_filtrado.groupby("Categoria")["Valor"].sum())

    st.subheader("Por mês")
    df_filtrado["Mes"] = df_filtrado["Data"].dt.to_period("M").astype(str)
    st.line_chart(df_filtrado.groupby("Mes")["Valor"].sum())

    st.subheader("Últimos gastos")
    st.dataframe(df_filtrado.sort_values("Data", ascending=False))
    

if __name__ == "__main__":
    renderizar_dashboard()