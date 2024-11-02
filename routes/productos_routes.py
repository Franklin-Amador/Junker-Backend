from fastapi import APIRouter, HTTPException
from controllers.productos_controller import get_productos, create_producto, update_producto, delete_producto, get_UnProducto
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete

router = APIRouter()

@router.get("/productos")
async def obtener_productos():
    productos = get_productos()
    return productos 

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
    
    