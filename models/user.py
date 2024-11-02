from datetime import date
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    
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
    user_info: dict

class UserUpdate(BaseModel):
    nombre: str
    apellido: str
    genero: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    avatar_url: Optional[str] = None