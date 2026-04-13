from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health",     summary="Verifica o status da API",
    description="""
Retorna o status atual da API, indicando se o serviço está disponível.
"""
)
def health_check():
    return {
        "status": "ok",
        "service": "walleto-api"
    }

