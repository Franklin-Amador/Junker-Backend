from pydantic import BaseModel

class CategoryCreate(BaseModel):
    nombre: str
    
class CategoryUpdate(BaseModel):
    id: int
    nombre: str
    
class CategoryDelete(BaseModel):
    id: int