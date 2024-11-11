from pydantic import BaseModel, Field
from typing import List

class CarritoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=70)
    descripcion: str = Field(..., min_length=1, max_length=1000)
    precio: float
    estado_producto: str = Field(..., min_length=1, max_length=50)
    imagen_url: List[str]
    stock: int
    id_producto: str
    id_carrito: str
    cantidad:int  
    
class CarritoUpdate(BaseModel):
    id:str
    nombre: str = Field(..., min_length=1, max_length=70)
    descripcion: str = Field(..., min_length=1, max_length=1000)
    precio: float
    estado_producto: str = Field(..., min_length=1, max_length=50)
    imagen_url: List[str]
    stock: int
    id_producto: str
    id_carrito: str
    cantidad:int  
    
class CarritoDelete(BaseModel):
    id: str

class CarritoRead(BaseModel):
    id: str