from fastapi import APIRouter, HTTPException, Response, status
from db.supabase import supabase_manager 
from models.user import UserCreate, UserLogin, PasswordReset, Logout, NewPasswordRequest
from controllers.password_controller import PasswordController
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PasswordResetRequest(BaseModel):
    new_password: str
    access_token: str
    refresh_token: str
  

router = APIRouter()
password_controller = PasswordController()

@router.post("/register")
async def register(user: UserCreate):
    user_dict = user.model_dump()
    try:
        res = supabase_manager.client.from_("usuarios").insert(user_dict).execute()
        
        print(res)
        
        if not res:
            raise HTTPException(status_code=400, detail="User registration failed")
        
        return res
    
    except Exception as e:
        # Capturar errores específicos de Supabase y devolverlos
        raise HTTPException(status_code=400, detail=f"Supabase error: {str(e)}")
    
    
@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase_manager.sign_in(user.email, user.password)
        usuario = response.user.id
        session = response.session
        # data = supabase_manager.get_user_info(usuario)
        data = supabase_manager.client.rpc('user_info', {'user_id': usuario}).execute()
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user": usuario,
            "data": data.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  
@router.post("/logout")
async def logout(tokens: Logout):
    try:
        response = supabase_manager.sign_out(tokens)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

        
    # ! Punto critico
@router.post("/new-reset")
async def new_pass(data: PasswordResetRequest) -> Dict[str, str]:
    try:
        # Paso 1: Establecer la sesión con los tokens
        session = supabase_manager.get_session(data.access_token, data.refresh_token)
        
        # Paso 2: Actualizar la contraseña
        result = supabase_manager.update_password(session, data.new_password)
        
        return {"message": "Contraseña actualizada! Seras redirigido en 3 segundos..."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/forgot")
async def forgot(data: PasswordReset):
    try:
        mail = supabase_manager.reset_password(data.email)
        
        return {"message": "Correo de restablecimiento enviado!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



    
