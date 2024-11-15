from fastapi import APIRouter, Depends
from controllers.usuarios_controller import actualizar_correo, actualizar_usuario, obtener_usuario, verify_token, AuthController, actualizar_desc, verificar_contra
from models.user import UserUpdate, UpdateEmail, UpdateDescripcion, UpdatePassword
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict

router = APIRouter()
security = HTTPBearer()

@router.get('/getUser/{user_id}')
async def get_user(user_id: str):
    return obtener_usuario(user_id)

@router.put("/updateUser/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, user: dict = Depends(verify_token)):
    return actualizar_usuario(user_id, user_data, user)

@router.put("/updateEmail/{user_id}")
async def update_email(user_id: str, email: UpdateEmail, user: dict = Depends(verify_token)):
    return actualizar_correo(user_id, email, user)

@router.put("/updateDescripcion/{user_id}")
async def update_desc(user_id: str, descripcion: UpdateDescripcion, user: dict = Depends(verify_token)):
    return actualizar_desc(user_id, descripcion)