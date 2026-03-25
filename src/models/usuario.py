from dataclasses import dataclass
from datetime import date

@dataclass
class Usuario:
    nome: str
    email: str
    data_nascimento: date
    sexo: str | None
    id: int | None
    senha_hash: int | None
