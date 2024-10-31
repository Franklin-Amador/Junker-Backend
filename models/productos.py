from pydantic import BaseModel

class ProductosCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen_url: str
    id_vendedor:str    
    
class ProductosUpdate(BaseModel):
    id:str
    nombre: str
    descripcion: str
    precio: float 
    imagen_url: str 
    id_vendedor:str 
    
class ProductosDelete(BaseModel):
    id: str
    
class ProductoRead(BaseModel):
    id: str