from pydantic import BaseModel, Field
from typing import List

class ProductosCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=70)
    descripcion: str = Field(..., min_length=1, max_length=1000)
    precio: float
    estado_producto: str = Field(..., min_length=1, max_length=50)
    imagen_url: List[str]
    stock: int
    id_vendedor: str
    id_categoria: str   
    
class ProductosUpdate(BaseModel):
    id:str
    nombre: str = Field(..., min_length=1, max_length=70)
    descripcion: str = Field(..., min_length=1, max_length=1000)
    precio: float 
    estado_producto: str = Field(..., min_length=1, max_length=50)
    stock: int
    imagen_url: List[str]
    id_vendedor:str 
    
class ProductosDelete(BaseModel):
    id: str
    
class ProductoRead(BaseModel):
    id: str