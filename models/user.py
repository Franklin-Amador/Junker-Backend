from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[str] = None
    telefono: Optional[str] = None
    genero: Optional[str] = None
    direccion: Optional[str] = None
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class PasswordReset(BaseModel):
    email: str
    
class Logout(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    user_info: dict  # Puedes ajustar esto según lo que necesites