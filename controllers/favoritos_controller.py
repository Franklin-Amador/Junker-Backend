from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.favoritos import FavoritoRead, FavoritoCreate, FavoritoUpdate, FavoritoDelete

# * Ver todos los articulos en favoritos
def get_favoritos(usuario_id: FavoritoRead):
    try:
        favoritos = supabase_manager.client.from_("favoritos").select(
            "*, productos(*, productos_imagenes_filtradas(url), vendedores(calificacion, usuarios(nombre, apellido, avatar_url)))"
            ).eq("id_usuario", usuario_id).execute()
        return favoritos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# * Agregar a favoritos
def create_favoritos(favorito: FavoritoCreate):
    try:
        data_favorito = {
            "id_usuario": favorito.id_usuario,
            "id_producto": favorito.id_producto,    
        }
        
        favorito_res = supabase_manager.client.from_("favoritos").insert(data_favorito).execute() 
        
        if not favorito_res.data:
            raise HTTPException(status_code=400, detail="Error al crear el favorito")        
        
        return {"message": "favorito creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# * Actualizar productos
def update_favoritos(favorito: FavoritoUpdate):
    try:
        data = {
            "id_favorito": favorito.id_favorito,
            "id_producto": favorito.id_producto,
            "cantidad": favorito.cantidad,
        }
        
        favorito_update = supabase_manager.client.from_("favoritos").update(data).eq("id",favorito.id).execute()
       
        if not favorito_update.data:
            raise HTTPException(status_code=400, detail="Error al actualizar la imagen del favorito")
       
        return {"message": "favorito actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Eliminar un favorito
def delete_favoritos(usuario_id: FavoritoDelete, producto_id: str):
    try:
        # * Eliminar datos
        respuesta = supabase_manager.client.from_("favoritos").delete().eq("id_usuario",usuario_id).eq("id_producto", producto_id).execute()
        
        if respuesta.data is None or len(respuesta.data) == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
        
        return {"message": "El producto ha sido eliminado correctamente de los favoritos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

