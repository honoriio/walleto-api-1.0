# Área destinada a importações
import datetime
import re

def validar_e_converter_data(data_str: str) -> datetime.date:
    """
    Tenta converter uma string de data (formatos DD/MM/AAAA ou DDMMAAAA) 
    em um objeto date. Levanta ValueError se inválido.
    """
    # 1. Normalizar separadores (substitui '.', '-', '_' por '/')
    # re.sub é mais eficiente que múltiplos .replace()
    data_limpa = re.sub(r"[.\-_]", "/", data_str)

    # 2. Tratar formato sem separador (DDMMAAAA)
    if len(data_limpa) == 8 and data_limpa.isdigit():
        data_limpa = f"{data_limpa[0:2]}/{data_limpa[2:4]}/{data_limpa[4:8]}"
    
    # 3. Tentar converter para data e retornar o objeto date
    try:
        return datetime.datetime.strptime(data_limpa, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError(f"Formato de data '{data_str}' inválido ou data não existe.")