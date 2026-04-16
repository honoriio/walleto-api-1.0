import os
import requests
import pandas as pd
import streamlit as st


def formatar_moeda_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados_api(token: str) -> pd.DataFrame:
    API_URL = os.getenv("API_URL")

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{API_URL}/dashboard/dados", headers=headers)

    if response.status_code != 200:
        raise Exception("Erro ao buscar dados da API")

    dados = response.json().get("gastos", [])
    df = pd.DataFrame(dados)

    if df.empty:
        return df

    
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Categoria"] = df["Categoria"].fillna("Sem categoria")
    df["Descrição"] = df.get("Descrição", "").fillna("")

    df = df.dropna(subset=["Valor", "Data"])

    return df


def renderizar_dashboard():
    st.set_page_config(page_title="Walleto Dashboard", layout="wide")

    token = st.query_params.get("token")

    if not token:
        st.error("Acesso não autorizado")
        st.stop()

    try:
        df = carregar_dados_api(token)
    except Exception as e:
        st.error(f"Erro: {e}")
        st.stop()

    if df.empty:
        st.warning("Sem dados")
        return

    st.title("Dashboard Financeiro")

    
    col1, col2 = st.columns(2)

    categorias = sorted(df["Categoria"].unique())
    categorias_sel = col1.multiselect("Categoria", categorias, default=categorias)

    data_min = df["Data"].min()
    data_max = df["Data"].max()

    datas = col2.date_input("Período", (data_min, data_max))

    df_filtrado = df[df["Categoria"].isin(categorias_sel)]

    if isinstance(datas, tuple) and len(datas) == 2:
        inicio, fim = pd.to_datetime(datas[0]), pd.to_datetime(datas[1])
        df_filtrado = df_filtrado[
            (df_filtrado["Data"] >= inicio) & (df_filtrado["Data"] <= fim)
        ]

    
    total = df_filtrado["Valor"].sum()
    qtd = len(df_filtrado)
    ticket = df_filtrado["Valor"].mean() if qtd > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total gasto", formatar_moeda_brl(total))
    c2.metric("Quantidade", qtd)
    c3.metric("Ticket médio", formatar_moeda_brl(ticket))

    st.divider()

    
    st.subheader("Por categoria")
    cat = df_filtrado.groupby("Categoria")["Valor"].sum()
    st.bar_chart(cat)

    st.subheader("Por mês")
    df_filtrado["Mes"] = df_filtrado["Data"].dt.to_period("M").astype(str)
    mes = df_filtrado.groupby("Mes")["Valor"].sum()
    st.line_chart(mes)

    
    st.subheader("Dados")
    st.dataframe(df_filtrado)


if __name__ == "__main__":
    renderizar_dashboard()