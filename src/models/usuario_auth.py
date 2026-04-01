from dataclasses import dataclass

@dataclass
class UsuarioAuth:
    id: int
    email: str
    senha_hash: str