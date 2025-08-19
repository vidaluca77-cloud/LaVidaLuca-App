from supabase import create_client, Client
from app.config import settings

def get_supabase_client() -> Client:
    """Create and return a Supabase client instance."""
    return create_client(settings.supabase_url, settings.supabase_anon_key)

def get_supabase_admin_client() -> Client:
    """Create and return a Supabase admin client instance."""
    return create_client(settings.supabase_url, settings.supabase_service_role_key)