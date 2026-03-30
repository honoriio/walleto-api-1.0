from dataclasses import dataclass
from datetime import date


@dataclass
class Usuario:
    nome: str
    email: str
    data_nascimento: date
    senha_hash: str
    sexo: str | None = None
    id: int | None = None