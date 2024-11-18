from pydantic import BaseModel, field_validator
from utils.globals import validate_sql_injection
from typing import Optional
from datetime import datetime
import re

class UserCreate(BaseModel):
    id: str
    nombre: str
    apellido: str
    email: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
    @field_validator('email')
    def email_length(cls, v):
        if validate_sql_injection(v):
            raise ValueError('Invalid email')
        return v
    
class PasswordReset(BaseModel):
    email: str
    
class Logout(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    user_info: dict 
    
class MailSend(BaseModel):
    email: str
    
class NewPasswordRequest(BaseModel):
    token: str
    new_password: str

class ResetToken(BaseModel):
    email: str
    token: str
    created_at: datetime
    expires_at: datetime
    
class UserUpdate(BaseModel):
    nombre: str
    apellido: str
    genero: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    direccion: Optional[str] = None
    avatar_url: Optional[str] = None
    telefono: Optional[str] = None
    
class UpdateEmail(BaseModel):
    email: str
    
class UpdateDescripcion(BaseModel):
    descripcion: str
    
class UpdatePassword(BaseModel):
    password: str
    newPassword: str
    
class ProductosVendedor(BaseModel):
    id: str
    nombre: str
    descripcion: str
    precio: str
    estado: str