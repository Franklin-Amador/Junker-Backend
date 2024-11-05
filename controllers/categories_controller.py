from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.categories import CategoryCreate, CategoryUpdate, CategoryDelete

# * Crear categoría
async def create_category(category: CategoryCreate):
    try:
        data = {
            "nombre": category.nombre,
        }
        
        result = supabase_manager.client.from_("prueba2").insert(data).execute()
        
        return {"message": "Categoria creada correctamente", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear categoría: {str(e)}")
    
# * Actualizar categoría
def update_category(category: CategoryUpdate):
    try:
        # * Acutalizar datos 
        data = {
            "nombre": category.nombre
        }
        
        supabase_manager.client.from_("categorias").update(data).eq("id",category.id).execute()
        return {"message": "Categoria actulizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Eliminar categoría
def delete_category(category: CategoryDelete):
    try:
        # * Eliminar datos
        supabase_manager.client.from_("categorias").delete().eq("id",category.id).execute()
        return {"message": "Categoria eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
