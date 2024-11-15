from fastapi import APIRouter, Query, HTTPException	
from controllers.productos_controller import create_producto, update_producto, delete_producto, get_UnProducto, ProductFilter, ProductQuery
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete
from typing import Optional



router = APIRouter()

# * Endpoint de get paginado con filtro de categoría v7
@router.get("/productos")
async def obtener_productos(
    page: int = 1,
    limit: int = 16,
    categoria: Optional[str] = None,
    precio_min: Optional[int] = None,
    precio_max: Optional[int] = None,
    estado: Optional[str] = None
):
    try:
        offset = (page - 1) * limit
        filters = ProductFilter(categoria, precio_min, precio_max, estado)
        
        # Obtener productos y total en paralelo
        productos = await ProductQuery.get_productos(offset, limit, filters)
        total = await ProductQuery.count_productos(filters)
        
        return {
            "items": productos,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit),  # Redondeo hacia arriba
            "filters_applied": {
                "categoria": categoria,
                "precio_min": precio_min,
                "precio_max": precio_max,
                "estado": estado
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    
    