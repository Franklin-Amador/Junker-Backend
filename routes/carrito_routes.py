from fastapi import APIRouter
from controllers.carrito_controller import get_carrito, create_carrito, update_carrito, delete_carrito, get_Uncarrito
from models.carrito import CarritoCreate, CarritoUpdate, CarritoDelete
# from typing import Optional

router = APIRouter()

@router.get("/carrito/{carrito_id}")
async def obtener_carrito(carrito_id: str): 
    carritos = get_carrito(carrito_id)  
    return  carritos

@router.get("/carrito/{carrito_id}, {producto_id},")
async def obtener_carrito(carrito_id: str, producto_id: str):
    return get_Uncarrito(carrito_id, producto_id)

     
@router.post("/carrito")
async def post_carritos(carrito: CarritoCreate):
    return create_carrito(carrito)

@router.put("/carrito")
async def put_carrito(carrito: CarritoUpdate):
    return update_carrito(carrito)

@router.delete("/carrito")
async def borrar_carrito(carrito: CarritoDelete):
    return delete_carrito(carrito)
    
    