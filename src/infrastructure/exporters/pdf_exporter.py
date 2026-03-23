from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)

from src.core.config import PASTA_DOCUMENTOS
from src.infrastructure.exporters.excel_exporter import (
    normalizar_gastos,
    calcular_resumo_gastos,
)


def formatar_moeda_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def criar_tabela_gastos(registros_normalizados, total_gastos):
    dados = [["Nome", "Valor", "Categoria", "Data", "Descrição"]]

    for registro in registros_normalizados:
        dados.append([
            registro["nome"],
            formatar_moeda_brl(registro["valor"]),
            registro["categoria"],
            registro["data"],
            registro["descricao"],
        ])

    dados.append([
        "TOTAL",
        formatar_moeda_brl(total_gastos),
        "",
        "",
        "",
    ])

    tabela = Table(
        dados,
        colWidths=[4.5 * cm, 3 * cm, 4 * cm, 3 * cm, 8 * cm]
    )

    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#D9EAF7")]),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#C6E0B4")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ])

    tabela.setStyle(estilo)
    return tabela


def criar_tabela_resumo(resumo_dados):
    categorias = sorted(
        set(
            list(resumo_dados["totais_mes"].keys()) +
            list(resumo_dados["totais_ano"].keys())
        )
    )

    dados = [["Categoria", "Total Mês", "Total Ano"]]

    for categoria in categorias:
        dados.append([
            categoria,
            formatar_moeda_brl(resumo_dados["totais_mes"].get(categoria, 0)),
            formatar_moeda_brl(resumo_dados["totais_ano"].get(categoria, 0)),
        ])

    tabela = Table(dados, colWidths=[7 * cm, 4 * cm, 4 * cm])

    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#D9EAF7")]),
    ])

    tabela.setStyle(estilo)
    return tabela


def exportar_gastos_pdf(gastos):
    styles = getSampleStyleSheet()

    registros_normalizados, meses = normalizar_gastos(gastos)
    resumo_dados = calcular_resumo_gastos(registros_normalizados)

    mes_nome = meses[0] if meses else "sem_mes"

    PASTA_DOCUMENTOS.mkdir(parents=True, exist_ok=True)

    nome_arquivo = f"despesas_{mes_nome}.pdf"
    caminho_completo = PASTA_DOCUMENTOS / nome_arquivo

    doc = SimpleDocTemplate(
        str(caminho_completo),
        pagesize=landscape(A4),
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
    )

    elementos = []

    elementos.append(Paragraph("Relatório de Despesas", styles["Title"]))
    elementos.append(Spacer(1, 0.5 * cm))
    elementos.append(criar_tabela_gastos(
        registros_normalizados,
        resumo_dados["total_gastos"]
    ))

    elementos.append(PageBreak())

    titulo_resumo = (
        f"Resumo de Categorias - "
        f"Mês {resumo_dados['mes_principal']:02d}/{resumo_dados['ano_principal']}"
    )
    elementos.append(Paragraph(titulo_resumo, styles["Title"]))
    elementos.append(Spacer(1, 0.5 * cm))
    elementos.append(criar_tabela_resumo(resumo_dados))

    doc.build(elementos)

    return str(caminho_completo)    