from config.config import SUPABASE_KEY, SUPABASE_URL
from supabase import Client, create_client
from typing import Any
import logging

# def get_supabase_client() -> Client:
#     return create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurar logging
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


try:
    supabase_manager = SupabaseManager()
    logger.info("SupabaseManager instance created successfully")
except Exception as e:
    logger.error(f"Failed to create SupabaseManager instance: {str(e)}")
    supabase_manager = None