from pydantic import BaseModel, Field
from typing import List

class CarritoCreate(BaseModel):
    id_producto: str
    id_carrito: str
    cantidad:int = Field(..., gt=0, description="La cantidad debe ser mayor a cero")  
    
class CarritoUpdate(BaseModel):
    id:str
    id_producto: str
    id_carrito: str
    cantidad:int = Field(..., gt=0, description="La cantidad debe ser mayor a cero")  
    
class CarritoDelete(BaseModel):
    id: str

class CarritoRead(BaseModel):
    id: str