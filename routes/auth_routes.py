from fastapi import APIRouter, HTTPException
from db.supabase import supabase_manager 
from models.user import UserCreate, UserLogin, PasswordReset, Logout


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    try:
        # ? Registrarse en Supabase
        response = supabase_manager.sign_up(user.email, user.password)

        # ? verificar si el usuario se registró correctamente 
        if response.user: 
            user_id = response.user.id

            # * Guardar datos en la tabla de usuarios
            user_data = {
                "id": user_id,  
                "nombre": user.nombre,
                "apellido": user.apellido,
                "telefono": user.telefono,
                "genero": user.genero,
                "direccion": user.direccion,
                "email": user.email,
                "fecha_nacimiento": user.fecha_nacimiento
            }

            # * Insertar datos en la tabla de usuarios
            supabase_manager.client.from_("usuarios").insert(user_data).execute()

            return {"message": "User registered successfully", "user": response.user}
        
        else:
            raise HTTPException(status_code=400, detail="User registration failed")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase_manager.sign_in(user.email, user.password)
        session = response.session
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/logout")
async def logout(tokens: Logout):
    try:
        response = supabase_manager.sign_out(tokens)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    