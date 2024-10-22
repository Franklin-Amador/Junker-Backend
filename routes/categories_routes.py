from fastapi import APIRouter, HTTPException
from db.supabase import supabase_manager 
from controllers.categories import create_category, update_category, delete_category
from models.categories import CategoryCreate, CategoryUpdate, CategoryDelete

router = APIRouter()

@router.get("/categories")
async def get_categories():
    try:
        categories = supabase_manager.client.from_("categorias").select("*").execute()
        return categories.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/categories")
async def post_categories(category: CategoryCreate):
    return create_category(category)

@router.patch("/categories")
async def patch_categories(category: CategoryUpdate):
    return update_category(category)

@router.delete("/ctegories")
async def delete_categories(category: CategoryDelete):
    return delete_category(category)
    
    