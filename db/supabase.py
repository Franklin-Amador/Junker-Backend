from config.config import SUPABASE_KEY, SUPABASE_URL
from supabase import Client, create_client
from typing import Any, Dict
import logging
from pydantic import BaseModel
import time

class TokenData(BaseModel):
    access_token: str
    refresh_token: str

# * Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        url: str = SUPABASE_URL
        key: str = SUPABASE_KEY
        self.client: Client = create_client(url, key)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def sign_up(self, email: str, password: str) -> Any:
        return self.client.auth.sign_up({"email": email, "password": password})

    def sign_in(self, email: str, password: str) -> Any:
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def sign_out(self, tokens: TokenData) -> Dict[str, str]:
        try:
            # * Establecemos la sesión del usuario
            self.client.auth.set_session(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
                
            )

            self.client.auth.sign_out()
            return {"message": "Sesión cerrada exitosamente"}
        except Exception as e:
            logger.error(f"Error en sign_out: {str(e)}")
            raise Exception(f"Error al cerrar sesión: {str(e)}")
   
    def get_user_info(self, user_id: str) -> Any:
        return self.client.table('usuarios').select("nombre").eq("email", user_id).execute()

    # ? Funciones de reestablecer contraseña
    def save_reset_token(self, email: str, token: str, created_at: str, expires_at: str):
        return self.client.table('reset_tokens').insert({
            'email': email,
            'token': token,
            'created_at': created_at,
            'expires_at': expires_at
        }).execute()

    def get_reset_token(self, token: str):
        return self.client.table('reset_tokens').select('*').eq('token', token).execute()

    def delete_reset_token(self, token: str):
        return self.client.table('reset_tokens').delete().eq('token', token).execute()
      
    def update_user_password(self, email: str, new_password: str):
        try:
            return self.client.auth.reset_password_email(email)
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            raise Exception(f"Error al actualizar la contraseña: {e}")
        
    def reset_password(self, email:str):
        try:
            return self.client.auth.reset_password_email(email)
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            raise Exception(f"Error al actualizar la contraseña: {e}")
        
# ! Punto critico
    
    def get_session(self, access_token: str, refresh_token: str) -> Dict[str, Any]:
        try:
            # Usar directamente los tokens proporcionados
            self.client.auth.set_session(access_token, refresh_token)
            
            # Obtener la sesión actual
            session = self.client.auth.get_session()
            
            if not session:
                raise Exception("Failed to get valid session")
                
            return {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token
            }
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")
        

    def update_password(self, session: Dict[str, str], new_password: str) -> Dict[str, Any]:
        try:
            # Actualizar la contraseña usando el método oficial de Supabase
            result = self.client.auth.update_user({"password": new_password})
            
            if not result.user:
                raise Exception("Failed to update password")
                
            return {"status": "success", "message": "Password updated successfully"}
        except Exception as e:
            raise Exception(f"Password update failed: {str(e)}")


try:
    supabase_manager = SupabaseManager()
    logger.info("SupabaseManager instance created successfully")
except Exception as e:
    logger.error(f"Failed to create SupabaseManager instance: {str(e)}")
    supabase_manager = None