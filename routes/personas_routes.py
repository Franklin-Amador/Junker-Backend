from fastapi import APIRouter
from db.supabase import supabase_manager

router = APIRouter()

@router.get("/personas/")
async def get_personas():
    try:
        # Hacer un select de todos los registros en la tabla personas
        response = supabase_manager.getSession()
        usuario = supabase_manager.client.from_('usuarios').select('*').eq('id', response.user.id).execute()
    except Exception as e:
        return {"error": str(e)}