from dataclasses import dataclass
from datetime import date

@dataclass
class Usuario:
    nome: str
    email: str
    senha_hash: str
    sexo: str
    data_nascimento: date
    id: int | None = None