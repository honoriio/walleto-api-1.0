from dataclasses import dataclass
from datetime import date

@dataclass
class Usuario:
    nome: str
    email: str
    data_nascimento: date
    sexo: str
    senha_hash: str | None = None  
    id: int | None = None