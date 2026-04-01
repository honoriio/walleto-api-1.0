from fastapi import APIRouter, HTTPException, Depends
from src.api.schemas.auth_schema import AuthLoginRequest, AuthTokenResponse, AuthMeResponse
from src.services.auth_service import login_service, get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=AuthTokenResponse, status_code=200)
def login_usuario_api(dados_login: AuthLoginRequest):
    try:
        return login_service(dados_login)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))
    

@router.get("/me",response_model=AuthMeResponse ,status_code=200)
def buscar_usuario_logado_api(current_user=Depends(get_current_user)):
    return current_user
