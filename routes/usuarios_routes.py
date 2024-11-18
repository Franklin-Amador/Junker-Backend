from fastapi import APIRouter, Depends
from controllers.usuarios_controller import actualizar_usuario, obtener_usuario, actualizar_desc, obtener_productos
from models.user import UserUpdate, UpdateDescripcion, ProductosVendedor
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get('/getUser/{user_id}')
async def get_user(user_id: str):
    return obtener_usuario(user_id)

@router.put("/updateUser/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate):
    return actualizar_usuario(user_id, user_data)

@router.put("/updateDescripcion/{user_id}")
async def update_desc(user_id: str, descripcion: UpdateDescripcion):
    return actualizar_desc(user_id, descripcion)

@router.get("/getProductosVendedor/{id}")
async def get_productos(id: str):
    return obtener_productos(id)