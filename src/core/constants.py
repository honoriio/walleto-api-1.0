#==================================================================
#--------------------------LIMITES---------------------------------
#==================================================================


# =========================
#         LIMITES
# =========================

TAMANHO_LINHA = 160             # --> tAMANHO MAXIMO DAS LINHAS NA INTERFACE
CENTRALIZAR = 160
MAX_NOME_GASTO = 40             # --> TAMANHO MAXIMO DOS CARACTERES DO NOME DO GASTO
MAX_CATEGORIA_GASTO = 50        # --> TAMANHO MAXIMO DOS CARACTERES DA CATEGORIA GASTO
MAX_DESCRICAO_GASTO = 300       # --> TAMANHO MAXIMO DOS CARACTERES DA DESCRIÇÃO DO GASTO





# =========================
#  FUNÇÕES DE FORMATAÇÃO
# =========================

def linha(char: str = "-", tamanho: int = TAMANHO_LINHA) -> str:
    return char * tamanho


#==================================================================
#----------------------CORES E ESTILOS-----------------------------
#==================================================================



# =========================
# CORES ANSI - TEXTO NORMAL
# =========================

PRETO = "\033[30m"
VERMELHO = "\033[31m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
AZUL = "\033[34m"
MAGENTA = "\033[35m"
CIANO = "\033[36m"
BRANCO = "\033[37m"
RESET = "\033[0m"


# =========================
# TEXTO FORTE / BRILHANTE
# =========================

CINZA_ESCURO = "\033[90m"
VERMELHO_CLARO = "\033[91m"
VERDE_CLARO = "\033[92m"
AMARELO_CLARO = "\033[93m"
AZUL_CLARO = "\033[94m"
MAGENTA_CLARO = "\033[95m"
CIANO_CLARO = "\033[96m"
BRANCO_FORTE = "\033[97m"


# =========================
# CORES DE FUNDO (NORMAL)
# =========================

FUNDO_PRETO = "\033[40m"
FUNDO_VERMELHO = "\033[41m"
FUNDO_VERDE = "\033[42m"
FUNDO_AMARELO = "\033[43m"
FUNDO_AZUL = "\033[44m"
FUNDO_MAGENTA = "\033[45m"
FUNDO_CIANO = "\033[46m"
FUNDO_BRANCO = "\033[47m"


# =========================
# CORES DE FUNDO (BRILHANTE)
# =========================

FUNDO_CINZA_ESCURO = "\033[100m"
FUNDO_VERMELHO_CLARO = "\033[101m"
FUNDO_VERDE_CLARO = "\033[102m"
FUNDO_AMARELO_CLARO = "\033[103m"
FUNDO_AZUL_CLARO = "\033[104m"
FUNDO_MAGENTA_CLARO = "\033[105m"
FUNDO_CIANO_CLARO = "\033[106m"
FUNDO_BRANCO_FORTE = "\033[107m"


# =========================
#       ESTILOS
# =========================

NEGRITO = "\033[1m"
SUBLINHADO = "\033[4m"
INVERTIDO = "\033[7m"


# =========================
# ✅ EXEMPLO DE USO
# =========================

if __name__ == "__main__":
    print(f"{VERDE}Tudo certo!{RESET}")
    print(f"{VERMELHO}Erro ao processar.{RESET}")
    print(f"{NEGRITO}Texto em negrito{RESET}")
    print(f"{SUBLINHADO}Texto sublinhado{RESET}")
    print(f"{INVERTIDO}Texto invertido{RESET}")