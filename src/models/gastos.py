# área destinada as importaçoes
import uuid
from decimal import Decimal


# --- Definição da Classe Gasto ---
class Gasto:
    def __init__(self, nome, valor, categoria, descricao, data, id=None):

        # Lógica para o ID
        if id is None:
            self.id = str(uuid.uuid4())  # Se nenhum id foi passado, GERE um novo.
        else:
            self.id = id

        self.nome = nome
        self.valor = Decimal(valor) # --> como iremos usar valores monetarios, decidimos usar decimal.
        self.categoria = categoria
        self.descricao = descricao
        self.data = data
