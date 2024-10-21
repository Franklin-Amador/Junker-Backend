from fastapi import APIRouter, HTTPException
from db.supabase import supabase_manager 
from models.user import UserCreate, UserLogin

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    try:
        # Intentar registrar al usuario
        response = supabase_manager.sign_up(user.email, user.password)

        # Verificar si el registro fue exitoso
        if response.user:  # Si hay un usuario registrado
            # Obtener el id del usuario registrado
            user_id = response.user.id  # Asegúrate de que esto es correcto

            # Guardar la información adicional en Supabase
            user_data = {
                "id": user_id,  # Usar el mismo id en la tabla usuarios
                "nombre": user.nombre,
                "apellido": user.apellido,
                "telefono": user.telefono,
                "genero": user.genero,
                "direccion": user.direccion,
                "email": user.email,
                "fecha_nacimiento": user.fecha_nacimiento
            }

            # Insertar los datos en la tabla 'usuarios' en Supabase
            supabase_manager.client.from_("usuarios").insert(user_data).execute()  # Asegúrate de que este método sea correcto

            return {"message": "User registered successfully", "user": response.user}
        
        else:
            raise HTTPException(status_code=400, detail="User registration failed")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase_manager.sign_in(user.email, user.password)
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))