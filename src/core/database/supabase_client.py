import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# Chargement des variables d'environnement
load_dotenv()


class SupabaseManager:
    """
    Singleton pour gérer l'instance unique du client Supabase
    et encapsuler les appels réseau de manière thread-safe pour Flet.
    """
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                raise ValueError(
                    "⚠️ Les variables SUPABASE_URL et SUPABASE_KEY doivent être configurées dans le fichier .env")

            cls._instance = create_client(url, key)
        return cls._instance


# Fonction helper pour obtenir rapidement le client
def get_supabase() -> Client:
    return SupabaseManager.get_client()