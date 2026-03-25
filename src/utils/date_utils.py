# Área destinada a importações
from datetime import date, datetime
import re


def converter_data_ISO(data_str: str) -> str: #--> Ideal  para salvar no banco de dados
    return data_str.strftime("%Y-%m-%d")


def converter_data_brasil(data: str)-> date:  #--> Ideal para mostrar ao usuario, ja no formato brasleiro
    return datetime.datetime.strptime(data, "%d/%m/%Y").date()