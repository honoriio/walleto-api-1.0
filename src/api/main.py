from fastapi import FastAPI
from src.api.routes.dashboard_routes import router as dashboard_router
from src.api.routes.gasto_routes import router as gastos_router

app = FastAPI()

app.include_router(gastos_router)

app.include_router(dashboard_router)


