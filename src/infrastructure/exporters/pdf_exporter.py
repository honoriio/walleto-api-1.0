from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
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


def calcular_largura_colunas(
    dados: list[list[str]],
    fonte: str = "Helvetica",
    tamanho_fonte: int = 9,
) -> list[float]:
    larguras = [0] * len(dados[0])

    for linha in dados:
        for indice, celula in enumerate(linha):
            texto = str(celula)
            largura = stringWidth(texto, fonte, tamanho_fonte)
            larguras[indice] = max(larguras[indice], largura)

    # margem interna
    larguras = [largura + 10 for largura in larguras]

    return larguras


def ajustar_larguras_tabela_gastos(larguras: list[float]) -> list[float]:
    largura_total_disponivel = landscape(A4)[0] - (2 * cm)

    # limites mínimos e máximos por coluna
    largura_nome = min(max(larguras[0], 4.0 * cm), 6.5 * cm)
    largura_valor = 3.0 * cm
    largura_categoria = min(max(larguras[2], 3.5 * cm), 5.0 * cm)
    largura_data = 3.0 * cm

    largura_restante = (
        largura_total_disponivel
        - largura_nome
        - largura_valor
        - largura_categoria
        - largura_data
    )

    largura_descricao = max(largura_restante, 6.0 * cm)

    return [
        largura_nome,
        largura_valor,
        largura_categoria,
        largura_data,
        largura_descricao,
    ]


def criar_tabela_gastos(registros_normalizados, total_gastos):
    styles = getSampleStyleSheet()

    estilo_celula = ParagraphStyle(
        name="CelulaTabela",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        alignment=1,  # centralizado
        spaceAfter=0,
        spaceBefore=0,
    )

    estilo_cabecalho = ParagraphStyle(
        name="CabecalhoTabela",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        alignment=1,
        textColor=colors.white,
        spaceAfter=0,
        spaceBefore=0,
    )

    dados = [[
        Paragraph("Nome", estilo_cabecalho),
        Paragraph("Valor", estilo_cabecalho),
        Paragraph("Categoria", estilo_cabecalho),
        Paragraph("Data", estilo_cabecalho),
        Paragraph("Descrição", estilo_cabecalho),
    ]]

    dados_largura = [["Nome", "Valor", "Categoria", "Data", "Descrição"]]

    for registro in registros_normalizados:
        linha = [
            Paragraph(str(registro["nome"]), estilo_celula),
            Paragraph(formatar_moeda_brl(registro["valor"]), estilo_celula),
            Paragraph(str(registro["categoria"]), estilo_celula),
            Paragraph(str(registro["data"]), estilo_celula),
            Paragraph(str(registro["descricao"]), estilo_celula),
        ]
        dados.append(linha)

        dados_largura.append([
            str(registro["nome"]),
            formatar_moeda_brl(registro["valor"]),
            str(registro["categoria"]),
            str(registro["data"]),
            str(registro["descricao"]),
        ])

    dados.append([
        Paragraph("TOTAL", estilo_celula),
        Paragraph(formatar_moeda_brl(total_gastos), estilo_celula),
        Paragraph("", estilo_celula),
        Paragraph("", estilo_celula),
        Paragraph("", estilo_celula),
    ])

    dados_largura.append([
        "TOTAL",
        formatar_moeda_brl(total_gastos),
        "",
        "",
        "",
    ])

    larguras = calcular_largura_colunas(dados_largura, tamanho_fonte=9)
    larguras = ajustar_larguras_tabela_gastos(larguras)

    tabela = Table(
        dados,
        colWidths=larguras,
        repeatRows=1,
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
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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

    tabela = Table(dados, colWidths=[7 * cm, 4 * cm, 4 * cm], repeatRows=1)

    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#D9EAF7")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
    elementos.append(
        criar_tabela_gastos(
            registros_normalizados,
            resumo_dados["total_gastos"]
        )
    )

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