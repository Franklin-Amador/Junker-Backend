from fastapi import APIRouter, Query	
from controllers.productos_controller import get_productos, create_producto, update_producto, delete_producto, get_UnProducto, count_productos
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete
from typing import Optional



router = APIRouter()

# * Endpoint de get paginado
@router.get("/productos")
async def obtener_productos(page: int = 1, limit: int = 16):
    offset = (page - 1) * limit  # Calcular el desplazamiento
    productos = get_productos(offset, limit)
    total = count_productos()  # Contar el total de productos
    return {"items": productos, "total": total}


@router.get("/productos/{product_id}")
async def obtener_producto(product_id: str):
    return get_UnProducto(product_id)

     
@router.post("/productos")
async def post_productos(producto: ProductosCreate):
    return create_producto(producto)

@router.put("/productos")
async def put_productos(producto: ProductosUpdate):
    return update_producto(producto)

@router.delete("/producto")
async def delete_productos(producto: ProductosDelete):
    return delete_producto(producto)
    
    