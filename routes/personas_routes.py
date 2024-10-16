from fastapi import APIRouter
from db.supabase import get_supabase_client

router = APIRouter()
supabase = get_supabase_client()

@router.get("/personas/")
async def get_personas():
    try:
        # Hacer un select de todos los registros en la tabla personas
        response = supabase.table("personas").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}