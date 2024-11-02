from datetime import date
from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.user import UserUpdate

def obtener_usuario(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="ID de usuario no encontrado")

    response = supabase_manager.client.from_("usuarios").select("*").eq('id', user_id).single().execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return response.data

def actualizar_usuario(user_id: str, user_data: UserUpdate, token_user_id: str):
     # Verificar que el ID del usuario en el token coincida con el ID que se está actualizando
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar esta información")

    # Crear un diccionario de datos a actualizar excluyendo los valores no establecidos
    user_data_dict = user_data.model_dump(exclude_unset=True)
    
    # if isinstance(user_data_dict.get('fecha_nacimiento'), date):
    #     user_data_dict['fecha_nacimiento'] = user_data_dict['fecha_nacimiento'].isoformat()

    # Realizar la actualización en la tabla "usuarios"
    response_usuarios = supabase_manager.client.from_("usuarios").update(user_data_dict).eq('id', user_id).execute()

    if not response_usuarios.data:
        raise HTTPException(status_code=500, detail="Error al actualizar la información del usuario")

    # Si se actualizó el email, actualizar también en auth.users (opcional)
    # if user_data.email is not None:
    #     auth_update_data = {
    #         "email": user_data.email,
    #         "phone": user_data.telefono
    #     }
    #     response_auth = supabase_manager.client.from_("auth.users").update(auth_update_data).eq('id', user_id).execute()

    #     if not response_auth.data:
    #         raise HTTPException(status_code=500, detail="Error al actualizar la información en auth.users")

    return {"usuarios": response_usuarios.data[0]}