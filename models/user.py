from pydantic import BaseModel, field_validator
from utils.globals import validate_sql_injection
from typing import Optional
from datetime import datetime
import re

class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    
    @field_validator('password')
    def password_length(cls, v):
        if not re.search("[0-9]", v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search("[a-z]", v):
            raise ValueError('La contraseña debe contener al menos una letra')
        if not re.search("[A-Z]", v):
            raise ValueError('La contraseña debe contener al menos una letra mayuscula')
        if re.search(r'(012|123|234|345|456|567|678|789)', v):
            raise ValueError('La contraseña no puede contener una secuencia de 3 números consecutivos')
        return v
    
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