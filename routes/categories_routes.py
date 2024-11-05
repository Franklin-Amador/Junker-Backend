from fastapi import APIRouter, HTTPException
from db.supabase import supabase_manager 
from controllers.categories_controller import create_category, update_category, delete_category
from models.categories import CategoryCreate, CategoryUpdate, CategoryDelete, CategoryResponse

router = APIRouter()

@router.get("/categories")
async def get_categories():
    try:
        categories = supabase_manager.client.from_("categorias").select("*").execute()
        return categories.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/categories",
    response_model=CategoryResponse,
    responses={
        200: {
            "description": "Categoría creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Categoria creada correctamente",
                        "data": [{"nombre": "ejemplo"}]
                    }
                }
            }
        },
        422: {
            "description": "Error de validación - Datos inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "loc": ["body", "nombre"],
                            "msg": "ensure this value has at least 2 characters",
                            "type": "value_error.any_str.min_length"
                        }]
                    }
                }
            }
        },
        400: {
            "description": "Error al crear la categoría",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error al crear la categoría: detalles del error"
                    }
                }
            }
        }
    }
)
async def post_categories(category: CategoryCreate):
    return await create_category(category)

@router.patch("/categories")
async def patch_categories(category: CategoryUpdate):
    return update_category(category)

@router.delete("/categories")
async def delete_categories(category: CategoryDelete):
    return delete_category(category)
    
    