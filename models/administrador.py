from typing import Optional,  Any

from pydantic import BaseModel

class AsignarRol(BaseModel):
    id_usuario: str 
    id_rol: str  

class AdminFilter:
    def __init__(
        self,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        apellido: Optional[str] = None,
        rol: Optional[str] = None,
    ):
        self.nombre = nombre
        self.email = email
        self.apellido = apellido
        self.rol = rol

    def apply_filters(self, query: Any) -> Any:
        """Aplica todos los filtros configurados a la consulta"""
        if self.nombre is not None:
            query = query.gte("nombre", self.nombre)
        if self.rol is not None:
            query = query.gte("rol", self.rol)
        if self.apellido is not None:
            query = query.lte("apellido", self.apellido)
        if self.correo:
            query = query.eq("email", self.email)
        return query