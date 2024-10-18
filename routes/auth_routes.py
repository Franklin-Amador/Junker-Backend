from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase import supabase_manager 

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserCreate):
    try:
        response = supabase_manager.sign_up(user.email, user.password)
        return {"message": "User registered successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserCreate):
    try:
        response = supabase_manager.sign_in(user.email, user.password)
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))