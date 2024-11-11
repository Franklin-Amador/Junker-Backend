from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.carrito import CarritoCreate, CarritoUpdate, CarritoDelete, CarritoRead

# * Ver un producto en el carrito
def get_Uncarrito(carrito_id: CarritoRead):
    try:
        carrito = supabase_manager.client.from_("carrito_productos").select(
            "*"
            ).eq("id", carrito_id).single().execute()
        return carrito.data
    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))

# * Ver todos los articulos en el carrito
def get_carrito():
    try:
        carritos = supabase_manager.client.from_("carrito_productos").select(
            "*, carrito(id_usuario), productos(*, productos_imagenes(url, orden), vendedores(calificacion, usuarios(nombre, apellido)))"
            ).execute()
        return carritos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# * Crear un producto
def create_carrito(carrito: CarritoCreate):
    try:
        data_carrito = {
            "nombre": carrito.nombre,
            "descripcion": carrito.descripcion,
            "precio": carrito.precio,
            "estado_carrito": carrito.estado_carrito,
            "id_vendedor": carrito.id_vendedor,
            "stock": carrito.stock,       
        }
        
        carrito_res = supabase_manager.client.from_("carritos").insert(data_carrito).execute() 
        
        if not carrito_res.data:
            raise HTTPException(status_code=400, detail="Error al crear el carrito")        
        
        return {"message": "carrito creados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# * Actualizar productos
def update_carrito(carrito: CarritoUpdate):
    try:
        data = {
            "nombre": carrito.nombre,
            "descripcion": carrito.descripcion,
            "precio": carrito.precio,
            "id_vendedor": carrito.id_vendedor,
        }
        
        carrito_update = supabase_manager.client.from_("carrito_productos").update(data).eq("id",carrito.id).execute()
       
        if not carrito_update.data:
            raise HTTPException(status_code=400, detail="Error al actualizar la imagen del carrito")
       
        return {"message": "carrito actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Eliminar un carrito
def delete_carrito(carrito: CarritoDelete):
    try:
        # * Eliminar datos
        supabase_manager.client.from_("carrito_productos").delete().eq("id",carrito.id).execute()
        return {"message": "El carrito a sido eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
