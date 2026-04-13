from fastapi import FastAPI
import logging
from src.core.database import inicializar_banco
from src.core.logging_config import setup_logging
from contextlib import asynccontextmanager
from src.core.database import inicializar_banco
from src.api.routes.dashboard_routes import router as dashboard_router
from src.api.routes.gasto_routes import router as gastos_router
from src.api.routes.relatorio_routes import router as relatorio_router
from src.api.routes.usuarios_routes import router as usuarios_router
from src.api.routes.auth_routes import router as authlogin_router
from src.api.routes.health_routes import router as health_routes
from slowapi.errors import RateLimitExceeded
from src.core.rate_limiter import limiter
from src.core.rate_limiter_handler import rate_limit_handler



setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicação Walleto...")
    try:
        inicializar_banco()
        logger.info("Banco de dados inicializado com sucesso.")
    except Exception:
        logger.exception("Erro ao inicializar banco de dados.")
        raise

    yield

    logger.info("Encerrando aplicação Walleto...")


app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter

app.include_router(health_routes)

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.include_router(authlogin_router)

app.include_router(usuarios_router)

#app.include_router(gastos_router)

app.include_router(dashboard_router)

app.include_router(relatorio_router)
