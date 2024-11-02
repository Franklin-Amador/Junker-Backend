from config.config import SUPABASE_JWT_SECRET
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from controllers.usuarios_controller import actualizar_usuario, obtener_usuario
from models.user import UserUpdate
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

@router.get('/getUser')
async def get_user(user: dict = Depends(verify_token)):
    user_id = user.get('sub')
    return obtener_usuario(user_id)
    

@router.put("/updateUser/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, user: dict = Depends(verify_token)):
    token_user_id = user.get('sub')
    return actualizar_usuario(user_id, user_data, token_user_id)