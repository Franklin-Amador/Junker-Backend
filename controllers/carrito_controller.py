from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.carrito import CarritoCreate, CarritoUpdate, CarritoDelete, CarritoRead, ProductoId

# * Ver un producto en el carrito
def get_Uncarrito(carrito_id: CarritoRead, producto_id: ProductoId):

    try:
        carrito = supabase_manager.client.from_("carrito_productos").select(
            "cantidad"
            ).eq("id_carrito", carrito_id)\
            .eq("id_producto", producto_id)\
            .single()\
            .execute()
        return carrito.data.get("cantidad", 0) if carrito.data else 0
    except Exception:
        return 0

# * Ver todos los articulos en el carrito
def get_carrito(carrito_id: CarritoRead):
    try:
        carritos = supabase_manager.client.from_("carrito_productos").select(
            "*, carrito(id_usuario), productos(*, productos_imagenes_filtradas(url), vendedores(calificacion, usuarios(nombre, apellido, avatar_url)))"
            ).eq("id_carrito", carrito_id).execute()
        return carritos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# * Agregar al carrito
def create_carrito(carrito: CarritoCreate):
    try:
        data_carrito = {
            "id_carrito": carrito.id_carrito,
            "id_producto": carrito.id_producto,
            "cantidad": carrito.cantidad,     
        }
        
        carrito_res = supabase_manager.client.from_("carrito_productos").insert(data_carrito).execute() 
        
        if not carrito_res.data:
            raise HTTPException(status_code=400, detail="Error al crear el carrito")        
        
        return {"message": "carrito creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# * Actualizar productos
def update_carrito(carrito: CarritoUpdate):
    try:
        data = {
            "id_carrito": carrito.id_carrito,
            "id_producto": carrito.id_producto,
            "cantidad": carrito.cantidad,
        }
        
        carrito_update = supabase_manager.client.from_("carrito_productos").update(data).eq("id",carrito.id).execute()
       
        if not carrito_update.data:
            raise HTTPException(status_code=400, detail="Error al actualizar la imagen del carrito")
       
        return {"message": "carrito actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Eliminar un carrito
def delete_carrito(carrito_id: CarritoDelete, producto_id: str):
    try:
        # * Eliminar datos
        respuesta = supabase_manager.client.from_("carrito_productos").delete().eq("id_carrito",carrito_id).eq("id_producto", producto_id).execute()
        
        if respuesta.data is None or len(respuesta.data) == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
        
        return {"message": "El producto ha sido eliminado correctamente del carrito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
