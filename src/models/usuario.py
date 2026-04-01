from dataclasses import dataclass
from datetime import date

@dataclass
class Usuario:
    nome: str
    email: str
    data_nascimento: date
    sexo: str
    senha_hash: str | None = None     # abalisar o que fazer, acredito que não podemos deixar isso como opcional
    id: int | None = None