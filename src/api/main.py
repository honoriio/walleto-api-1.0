from fastapi import FastAPI
from src.api.routes.dashboard_routes import router as dashboard_router
from src.api.routes.gasto_routes import router as gastos_router
from src.api.routes.relatorio_routes import router as relatorio_router

app = FastAPI()

app.include_router(gastos_router)

app.include_router(dashboard_router)

app.include_router(relatorio_router)


