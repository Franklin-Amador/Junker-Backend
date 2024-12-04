from fastapi import APIRouter, HTTPException, Query
from controllers.administrador_controller import (
    Asignar_rol_usuario,
    RolesPermissions,
    get_roles,
    obtener_usuario_por_rol, 
    verificar_permisos,
    UsuarioQuery,
    AdminFilter, 
)
from typing import Optional

from models.administrador import AdminFilter, AsignarRol

router = APIRouter()



@router.get("/usuarios/filter")
async def obtener_los_usuarios(
    page: int = 1,
    limit: int = 16,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    email: Optional[str] = None,
    rol: Optional[str] = None,
    search_query: Optional[str] = "",
    sort_asc: Optional[bool] = None  # Parámetro opcional para el orden
):
    """
    Endpoint para obtener usuarios con filtros, búsqueda y ordenamiento opcional.
    """
    try:
        
        offset = (page - 1) * limit
        filters = AdminFilter(nombre, email, apellido, rol)
        
        # Obtener productos y total en paralelo, pasando search_query y sort_asc
        usuarios = await UsuarioQuery.get_usuarios(
            offset=offset,
            limit=limit,
            filters=filters,
            search_query=search_query,
            sort_asc=sort_asc  # Pasar el orden al método
        )
        total = await UsuarioQuery.count_usuarios(filters, search_query)
        
        return {
            "items": usuarios,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit),  # Cálculo del total de páginas
            "filters_applied": {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "rol": rol,
                "search_query": search_query,
                "sort_asc": sort_asc
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/roles/{user_id}")
async def listar_usuarios(user_id: str):
    return obtener_usuario_por_rol(user_id)

@router.get("/usuario/verificar-rol")
async def verificar_acceso(
    user_id: str = Query(..., description="ID del usuario a verificar"),
    rol: RolesPermissions = Query(..., description="Rol requerido para acceder")
):
    try:
        permisos = verificar_permisos(user_id, rol)
        return permisos
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    
@router.get("/roles")
async def obtener_roles():
    return get_roles()


@router.post("/rol")
async def post_rol_usuario(roles: AsignarRol):
    return Asignar_rol_usuario(roles)

