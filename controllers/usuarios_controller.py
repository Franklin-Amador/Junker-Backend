from config.config import SUPABASE_JWT_SECRET
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.supabase import supabase_manager 
from models.user import UserUpdate, UpdateEmail
import jwt

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
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decodificando el token: {str(e)}")

def obtener_usuario(user: dict = Depends(verify_token)):
    user_id = user.get('sub')

    if not user_id:
        raise HTTPException(status_code=401, detail="ID de usuario no encontrado")
    
    response = supabase_manager.client.from_("usuarios").select("*").eq('id', user_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return response.data

def actualizar_usuario(user_id: str, user_data: UserUpdate, user: dict):
    token_user_id = user.get('sub')
    
     # Verificar que el ID del usuario en el token coincida con el ID que se está actualizando
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar esta información")

    # Crear un diccionario de datos a actualizar excluyendo los valores no establecidos
    user_data_dict = user_data.model_dump(exclude_unset=True)

    # Realizar la actualización en la tabla "usuarios"
    response_usuarios = supabase_manager.client.from_("usuarios").update(user_data_dict).eq('id', user_id).execute()

    if not response_usuarios.data:
        raise HTTPException(status_code=500, detail="Error al actualizar la información del usuario")

    return {"usuarios": response_usuarios.data[0]}

def actualizar_correo(user_id: str, email: UpdateEmail, user: dict):
    token_user_id = user.get('sub')
    
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar esta información")
    
    response = supabase_manager.client.auth.update_user({"email": email.email})
    
    print(response)
    
    if not response:
        raise HTTPException(status_code=500, detail="Error al actualizar esta información")
    
    return response

# * clase para verificacion
class AuthController:
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials):
        token = credentials.credentials
        try:
            # Decodificar el token JWT con la clave secreta
            payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience=expected_audience)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error decodificando el token: {str(e)}")