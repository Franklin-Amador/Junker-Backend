from config.config import SUPABASE_JWT_SECRET
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.supabase import supabase_manager 
from models.user import UserUpdate, UpdateEmail, UpdateDescripcion
import jwt
from datetime import datetime, timedelta

# Clave secreta JWT de Supabase
SUPABASE_JWT_SECRET = SUPABASE_JWT_SECRET
expected_audience = "authenticated"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

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
    
    response = supabase_manager.client.from_("usuarios").select("*, vendedores(id, descripcion), carrito(id)").eq('id', user_id).single().execute()
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

    # Si 'fecha_nacimiento' está en el diccionario pero es una cadena vacía, cámbialo a None o elimínalo
    if user_data_dict.get("fecha_nacimiento") == "":
        user_data_dict["fecha_nacimiento"] = None  # O usa `del user_data_dict["fecha_nacimiento"]` para eliminarlo

    # Realizar la actualización en la tabla "usuarios"
    response_usuarios = supabase_manager.client.from_("usuarios").update(user_data_dict).eq('id', user_id).execute()

    if not response_usuarios.data:
        raise HTTPException(status_code=500, detail="Error al actualizar la información del usuario")

    return {"usuarios": response_usuarios.data[0]}


def actualizar_correo(user_id: str, email: UpdateEmail, user: dict):
    token_user_id = user.get('sub')
    
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar esta información")
    
    try:
        response = supabase_manager.client.auth.update_user({"email": email.email})
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def actualizar_desc(user_id: str, descripcion: UpdateDescripcion, user: dict):
    try:
        response = supabase_manager.client.from_('vendedores').update({
            'descripcion': descripcion.descripcion
        }).eq('id', user_id).execute()

        print(response)
        # Verifica si la actualización fue exitosa
        if response.status_code == 200:
            return {"success": True, "message": "Descripción actualizada correctamente"}
        else:
            return {"success": False, "message": "Error al actualizar la descripción"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

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
        
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SUPABASE_JWT_SECRET, algorithm=["HS256"])

    @staticmethod
    def create_refresh_token(data: dict):
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SUPABASE_JWT_SECRET, algorithm=["HS256"])

    @staticmethod
    async def refresh_access_token_logic(refresh_token: str):
        try:
            # Decodificar y verificar el refresh token
            payload = jwt.decode(refresh_token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Token inválido")
            
            # Verificar si el refresh token es válido en la base de datos de Supabase
            response = supabase_manager.client.from_("user_tokens").select("refresh_token").eq("user_id", user_id).single().execute()
            
            if not response.data or response.data["refresh_token"] != refresh_token:
                raise HTTPException(status_code=401, detail="Refresh token inválido o caducado")

            # Generar un nuevo access token
            new_access_token = AuthController.create_access_token({"sub": user_id})
            new_refresh_token = AuthController.create_refresh_token({"sub": user_id})

            # Actualizar el refresh token en la base de datos
            supabase_manager.client.from_("user_tokens").update({"refresh_token": new_refresh_token}).eq("user_id", user_id).execute()

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")