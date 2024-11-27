from pydantic import BaseModel

class FavoritoCreate(BaseModel):
    id_producto: str
    id_usuario: str
    
class FavoritoUpdate(BaseModel):
    id:str
    id_producto: str
    id_usuario: str
    
class FavoritoDelete(BaseModel):
    id_usuario: str
    id_producto: str

class FavoritoRead(BaseModel):
    id: str
    
class ProductoId(BaseModel):
    id: str    