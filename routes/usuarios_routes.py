from fastapi import APIRouter, Depends
from controllers.usuarios_controller import actualizar_correo, actualizar_usuario, obtener_usuario, verify_token, AuthController
from models.user import UserUpdate, UpdateEmail
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict

router = APIRouter()
security = HTTPBearer()

@router.get('/getUser')
async def get_user(user: dict = Depends(obtener_usuario)):
    return user

@router.put("/updateUser/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, user: dict = Depends(verify_token)):
    return actualizar_usuario(user_id, user_data, user)

@router.put("/updateEmail/{user_id}")
async def update_email(user_id: str, email: UpdateEmail, user: dict = Depends(verify_token)):
    return actualizar_correo(user_id, email, user)

@router.get("/verify", response_model=Dict)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = AuthController.verify_token(credentials)
    return {
        "valid": True,
        "user": payload.get("sub"),
        "exp": payload.get("exp")
    }