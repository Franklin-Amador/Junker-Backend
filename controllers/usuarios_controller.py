from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.user import UserUpdate, UpdateDescripcion, UpdatePassword

def obtener_usuario(user_id: str):

    if not user_id:
        raise HTTPException(status_code=401, detail="ID de usuario no encontrado")
    
    response = supabase_manager.client.from_("usuarios").select("*, vendedores(id, descripcion), carrito(id)").eq('id', user_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return response.data

def actualizar_usuario(user_id: str, user_data: UserUpdate):
    user_data_dict = user_data.model_dump(exclude_unset=True)

    if user_data_dict.get("fecha_nacimiento") == "":
        user_data_dict["fecha_nacimiento"] = None

    # Realizar la actualización en la tabla "usuarios"
    response_usuarios = supabase_manager.client.from_("usuarios").update(user_data_dict).eq('id', user_id).execute()

    if not response_usuarios.data:
        raise HTTPException(status_code=500, detail="Error al actualizar la información del usuario")

    return {"usuarios": response_usuarios.data[0]}
    
def actualizar_desc(user_id: str, descripcion: UpdateDescripcion):
    try:
        response = supabase_manager.client.from_('vendedores').update({
            'descripcion': descripcion.descripcion
        }).eq('id', user_id).execute()

        # Verifica si la actualización fue exitosa
        if response.status_code == 200:
            return {"success": True, "message": "Descripción actualizada correctamente"}
        else:
            return {"success": False, "message": "Error al actualizar la descripción"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def obtener_productos(id_vendedor: str, limit: int, offset: int):
    try:
        response = (
            supabase_manager
            .client
            .from_("productos")
            .select("id, nombre, productos_imagenes(url)")
            .eq("id_vendedor", id_vendedor)
            .limit(limit)
            .offset(offset)
            .order('fecha_publicacion', desc=True)
            .execute()
        )
        
        if response.data:
            productos = [
                {
                    "id": producto["id"],
                    "nombre": producto["nombre"],
                    "imagen": producto["productos_imagenes"][0]["url"] if producto.get("productos_imagenes") else None
                }
                for producto in response.data
            ]
            return productos
        else:
            # Retorna una lista vacía si no hay datos
            return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")
