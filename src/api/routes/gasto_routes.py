from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.validators.gasto_validator import validar_id_gasto, validar_nome_gasto, validar_valor_gasto, validar_categoria_gasto, validar_descricao_gasto, validar_data_gasto

router = APIRouter(prefix="/gastos", tags=["Gastos"])




