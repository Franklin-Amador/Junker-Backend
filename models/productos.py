from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

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
    nombre: Optional[str] = Field(None, min_length=1, max_length=70)
    descripcion: Optional[str] = Field(None, min_length=1, max_length=1000)
    precio: Optional[float] = None
    estado_producto: Optional[str] = Field(None, min_length=1, max_length=50)
    stock: Optional[int] = None
    imagen_url: Optional[List[str]] = None
    id_vendedor: Optional[str] = None
    
class ProductosDelete(BaseModel):
    id: str
    
class ProductoRead(BaseModel):
    id: str
    
class ProductFilter:
    def __init__(
        self,
        categoria: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        estado: Optional[str] = None
    ):
        self.categoria = categoria
        self.precio_min = precio_min
        self.precio_max = precio_max
        self.estado = estado

    def apply_filters(self, query: Any) -> Any:
        """Aplica todos los filtros configurados a la consulta"""
        if self.precio_min is not None:
            query = query.gte("precio", self.precio_min)
        if self.precio_max is not None:
            query = query.lte("precio", self.precio_max)
        if self.estado:
            query = query.eq("estado_producto", self.estado)
        return query