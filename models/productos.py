from pydantic import BaseModel

class ProductosCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen: str    
    
class ProductosUpdate(BaseModel):
    id:str
    nombre: str
    descripcion: str
    precio: float
    imagen: str    
    
class ProductosDelete(BaseModel):
    id: str