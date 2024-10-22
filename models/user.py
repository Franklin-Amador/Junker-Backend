from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[str] = None
    telefono: Optional[str] = None
    genero: Optional[str] = None
    direccion: Optional[str] = None
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PasswordReset(BaseModel):
    email: EmailStr