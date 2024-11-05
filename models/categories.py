from typing import Dict, List
from pydantic import BaseModel

# Modelo para la respuesta
class CategoryResponse(BaseModel):
    message: str
    data: List[Dict[str, str]]

# Tu modelo actual
class CategoryCreate(BaseModel):
    nombre: str


class CategoryUpdate(BaseModel):
    id: int
    nombre: str
    
class CategoryDelete(BaseModel):
    id: int