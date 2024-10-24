from fastapi import APIRouter, HTTPException
from db.supabase import supabase_manager 
from controllers.productos_controller import create_producto, update_producto, delete_producto
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete

router = APIRouter()

@router.get("/productos")
async def get_productos():
    try:
        productos = supabase_manager.client.from_("productos").select("*").execute()
        return productos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/productos")
async def post_productos(producto: ProductosCreate):
    return create_producto(producto)

@router.patch("/productos")
async def patch_productos(producto: ProductosUpdate):
    return update_producto(producto)

@router.delete("/producto")
async def delete_productos(producto: ProductosDelete):
    return delete_producto(producto)
    
    