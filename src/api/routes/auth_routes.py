from fastapi import APIRouter, HTTPException, Response
from src.api.schemas.auth_schema import AuthLoginRequest, AuthTokenResponse
from src.services.auth_service import login_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=AuthTokenResponse, status_code=200)
def login_usuario_api(dados_login: AuthLoginRequest):
    try:
        return login_service(dados_login)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))