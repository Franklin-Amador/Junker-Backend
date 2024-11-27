from pydantic import BaseModel, Field

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
    id_carrito: str
    id_producto: str

class CarritoRead(BaseModel):
    id: str
    
class ProductoId(BaseModel):
    id: str    