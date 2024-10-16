from config.config import SUPABASE_KEY, SUPABASE_URL
from supabase import Client, create_client

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)