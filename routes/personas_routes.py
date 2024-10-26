from config.config import SUPABASE_JWT_SECRET
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.supabase import supabase_manager
import jwt

router = APIRouter()

# Clave secreta JWT de Supabase
SUPABASE_JWT_SECRET = SUPABASE_JWT_SECRET
expected_audience = "authenticated"

# Middleware para obtener el token desde el header de la solicitud
security = HTTPBearer()

# Función para verificar el token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Decodificar el token JWT con la clave secreta
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience=expected_audience)
        return payload  # Retorna los datos del token decodificado
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decodificando el token: {str(e)}")

@router.get("/getUser/")
async def get_personas(user: dict = Depends(verify_token)):
    user_id = user.get('sub')  # Obtener el ID del usuario del token

    if not user_id:
        raise HTTPException(status_code=401, detail="ID de usuario no encontrado en el token")

    response = supabase_manager.client.from_("usuarios").select("*").eq('id', user_id).single().execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return response.data
