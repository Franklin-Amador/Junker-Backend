from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.categories import CategoryCreate, CategoryUpdate, CategoryDelete

# * Crear categoría
def create_category(category: CategoryCreate):
    try:
        # * Insertar datos en la tabla de categorías
        data = {
            "nombre": category.nombre,
        }
        
        supabase_manager.client.from_("categorias").insert(data).execute()  # Asegúrate de que este método sea correcto
        return {"message": "Categgria creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
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
    
