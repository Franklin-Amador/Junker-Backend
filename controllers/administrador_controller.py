from fastapi import HTTPException
from db.supabase import supabase_manager
from typing import Dict, Any, List, Optional

from enum import Enum
from typing import Union

from models.administrador import AdminFilter, AsignarRol

class RolesPermissions(str, Enum):
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"
    ADMINISTRADOR = "administrador"
    
    @classmethod
    def validar_rol(cls, rol: str) -> bool:
        return rol in cls._value2member_map_

# Type annotation for easier use
RolPermiso = Union[RolesPermissions, str]

def obtener_usuario_por_rol(user_id: str)-> Dict[str, Any]:

    if not user_id:
        raise HTTPException(status_code=401, detail="ID de usuario no encontrado")
    
    response = supabase_manager.client.from_("usuarios").select("*, roles_usuarios(roles(nombre))").eq('id', user_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return response.data


def verificar_permisos(user_id: str, rol_requerido: RolPermiso) -> dict:

    try:
        rol_str = rol_requerido.value if isinstance(rol_requerido, RolesPermissions) else rol_requerido
        
        usuario = obtener_usuario_por_rol(user_id)
        
        roles = [r['roles']['nombre'] for r in usuario.get('roles_usuarios', [])]
        tiene_permiso = rol_str in roles
        
        if not tiene_permiso:
            return {
                'permissions': False,
                'message': f'No tienes permisos de {rol_str} para acceder a esta página',
                'errorCode': 403
            }
        
        return {
            'permissions': True,
            'message': f'Cuenta con los permisos {rol_str}',
            'errorCode': 200,
            'usuario': usuario
        }
    
    except HTTPException as e:
        return {
            'permissions': False,
            'message': e.detail,
            'errorCode': e.status_code
        }
        
        
class UsuarioQuery:
    """Clase para manejar las consultas de usuarios"""
    BASE_SELECT = """
        id, apellido, nombre, email, avatar_url, estado
    """

    @staticmethod
    async def search_by_apellido(search_query: str) -> List[int]:
        """Busca usuarios por apellido"""
        try:
            query = supabase_manager.client.from_("usuarios")\
                .select("id")\
                .ilike("apellido", f"%{search_query}%")
            
            result = query.execute()
            return [item['id'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def search_by_nombre(search_query: str) -> List[int]:
        """Busca usuarios por nombre"""
        try:
            query = supabase_manager.client.from_("usuarios")\
                .select("id")\
                .ilike("nombre", f"%{search_query}%")
            
            result = query.execute()
            return [item['id'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def search_by_email(search_query: str) -> List[int]:
        """Busca usuarios por email"""
        try:
            query = supabase_manager.client.from_("usuarios")\
                .select("id")\
                .ilike("email", f"%{search_query}%")
            
            result = query.execute()
            return [item['id'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    async def get_filtered_roles_ids(rol: str) -> List[int]:
        """Obtiene los IDs de usuarios por rol"""
        try:
            subquery = supabase_manager.client.from_("roles_usuarios")\
                .select("id_usuario, roles!inner(nombre)")\
                .ilike("roles.nombre", f"%{rol}%")
            
            result = subquery.execute()
            return [item['id_usuario'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))    

    @classmethod
    async def get_usuarios(
        cls,
        offset: int,
        limit: int,
        filters: AdminFilter,
        search_query: str = "",
        sort_asc: Optional[bool] = None,
    ) -> List[Dict[Any, Any]]:
        try:
            # Consulta principal
            query = supabase_manager.client.from_("usuarios")\
                .select(cls.BASE_SELECT)

            # Si hay término de búsqueda, aplicar búsqueda
            if search_query:
                search_query = search_query.strip()
                nombre_ids = await cls.search_by_nombre(search_query)
                apellido_ids = await cls.search_by_apellido(search_query)
                email_ids = await cls.search_by_email(search_query)
                roles_ids = await cls.get_filtered_roles_ids(search_query) if search_query else []
            
                # Combinar todos los IDs encontrados y eliminar duplicados
                all_matching_ids = list(set(nombre_ids + apellido_ids + email_ids+ roles_ids))
            
                # Construir la consulta para buscar coincidencias
                if all_matching_ids:
                    query = query.in_("id", all_matching_ids)
                else:
                    query = query.or_(
                        f"nombre.ilike.%{search_query}%,apellido.ilike.%{search_query}%,email.ilike.%{search_query}%"
                    )

            if filters.rol and not search_query:
                usuarios_ids = await cls.get_filtered_roles_ids(filters.rol)
                if not usuarios_ids:
                    return []
                query = query.in_("id", usuarios_ids)
            
            # Aplicar filtros 
            if filters.nombre is not None:
                query = query.ilike("nombre", f"%{filters.nombre}%")
            
            if filters.apellido is not None:
                query = query.ilike("apellido", f"%{filters.apellido}%")
            
            if filters.email is not None:
                query = query.ilike("email", f"%{filters.email}%")  

            # Aplicar ordenamiento
            if sort_asc is not None:
                order_by = "nombre" if sort_asc else "nombre.desc"
                query = query.order(order_by)

            # Aplicar paginación
            query = query.range(offset, offset + limit - 1)

            # Ejecutar consulta principal
            result = query.execute()
            usuarios = result.data if result.data else []
            
            usuarios_response = []
            if usuarios:
                usuarios_ids = [p["id"] for p in usuarios]

                # Consulta de roles
                rol_query = supabase_manager.client.from_("roles_usuarios")\
                    .select("id_usuario, roles!inner(nombre)")\
                    .in_("id_usuario", usuarios_ids)

                # Ejecutar consultas en paralelo
                roles_result = rol_query.execute()


                roles_map = {}
                for rol in roles_result.data:
                    if rol["id_usuario"] not in roles_map:
                        roles_map[rol["id_usuario"]] = []
                    roles_map[rol["id_usuario"]].append(rol["roles"]["nombre"])
                
                # Construir respuesta final
                usuarios_response = [
                    {
                        "id": usuario["id"],
                        "nombre": usuario["nombre"],
                        "apellido": usuario["apellido"],
                        "rol": roles_map.get(usuario["id"], []),
                        "email": usuario["email"],
                        "avatar_url": usuario["avatar_url"],
                        "estado": usuario["estado"],
                        "telefono": usuario["telefono"],
                    }
                    for usuario in usuarios
                ]

            return usuarios_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def count_usuarios(cls, filters: AdminFilter, search_query: str = "") -> int:
        """Cuenta el total de usuarios con filtros y búsqueda aplicados"""
        try:
            query = supabase_manager.client.from_("usuarios")\
                .select("*", count="exact")

            # Si hay término de búsqueda, aplicar la misma lógica que en get_usuarios
            if search_query:
                search_query = search_query.strip()
                roles_ids = await cls.get_filtered_roles_ids(search_query)
                nombre_ids = await cls.search_by_nombre(search_query)
                apellido_ids = await cls.search_by_apellido(search_query)
                email_ids = await cls.search_by_email(search_query)
                
                all_matching_ids = list(set(nombre_ids + apellido_ids + email_ids + roles_ids))
                
                if all_matching_ids:
                    query = query.in_("id", all_matching_ids)
                else:
                    query = query.or_(
                        f"nombre.ilike.%{search_query}%,apellido.ilike.%{search_query}%,email.ilike.%{search_query}%"
                    )

            if filters.rol and not search_query:
                usuarios_ids = await cls.get_filtered_roles_ids(filters.rol)
                if not usuarios_ids:
                    return 0
                query = query.in_("id", usuarios_ids)
            
            # Aplicar filtros 
            if filters.nombre is not None:
                query = query.ilike("nombre", f"%{filters.nombre}%")
            
            if filters.apellido is not None:
                query = query.ilike("apellido", f"%{filters.apellido}%")
            
            if filters.email is not None:
                query = query.ilike("email", f"%{filters.email}%") 

            result = query.execute()
            return result.count if result.count is not None else 0
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
          

# * obtener roles 
def get_roles():
    try:
        roles = supabase_manager.client.from_("roles").select(
            "*"
            ).execute()
        return roles.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
def Asignar_rol_usuario(roles: AsignarRol):
    try:
        data_roles = {
            "id_usuario": roles.id_usuario,
            "id_rol": roles.id_rol,     
        }
        
        roles_res = supabase_manager.client.from_("roles_usuarios").insert(data_roles).execute() 
        
        if not roles_res.data:
            raise HTTPException(status_code=400, detail="Error al asignar rol")
        
        return {"message": "Rol asignado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    