from config.config import SUPABASE_KEY, SUPABASE_URL
from supabase import Client, create_client
from typing import Any, Dict
import logging
from pydantic import BaseModel

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

    def sign_up(self, email: str, password: str) -> Any:
        return self.client.auth.sign_up({"email": email, "password": password})

    def sign_in(self, email: str, password: str) -> Any:
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def sign_out(self, tokens: TokenData) -> Dict[str, str]:
        try:
            # * Establecemos la sesión del usuario
            self.client.auth.set_session(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token
            )

            self.client.auth.sign_out()
            return {"message": "Sesión cerrada exitosamente"}
        except Exception as e:
            logger.error(f"Error en sign_out: {str(e)}")
            raise Exception(f"Error al cerrar sesión: {str(e)}")

    def reset_password_for_email(self, email: str) -> Any:
        return self.client.auth.reset_password_email(email)



try:
    supabase_manager = SupabaseManager()
    logger.info("SupabaseManager instance created successfully")
except Exception as e:
    logger.error(f"Failed to create SupabaseManager instance: {str(e)}")
    supabase_manager = None