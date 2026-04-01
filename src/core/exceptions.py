class FiltroInvalidoError(Exception):
    """Erro para filtros inválidos."""

    def __init__(self, message: str = "Filtro inválido"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """Erro para recurso não encontrado."""

    def __init__(self, message: str = "Recurso não encontrado"):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, message: str = "Conflito de recurso"):
        self.message = message
        super().__init__(self.message)