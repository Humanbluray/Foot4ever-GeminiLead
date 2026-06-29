# src/features/auth/data/auth_service.py
from typing import Optional
from supabase import Client
from src.core.database.supabase_client import get_supabase
from src.features.auth.data.models import UserProfile


class AuthService:
    def __init__(self):
        self.client: Client = get_supabase()

    async def sign_in(self, email: str, password: str) -> Optional[UserProfile]:
        """Authentifie un utilisateur et récupère son profil public avec son rôle."""
        try:
            # Supabase API Call synchrone enveloppé ou exécuté directement
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if auth_response.user:
                user_id = auth_response.user.id
                return await self.get_user_profile(user_id)
            return None
        except Exception as e:
            print(f"❌ [AuthService.sign_in] Erreur: {e}")
            raise e

    async def sign_up(self, email: str, password: str, username: str) -> Optional[UserProfile]:
        """Crée un compte utilisateur avec un username stocké dans les metadata."""
        try:
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "role": "player"  # Rôle par défaut imposé par sécurité
                    }
                }
            })
            if auth_response.user:
                return await self.get_user_profile(auth_response.user.id)
            return None
        except Exception as e:
            print(f"❌ [AuthService.sign_up] Erreur: {e}")
            raise e

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Récupère les données de la table publique 'profiles'."""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).single().execute()
            if response.data:
                return UserProfile(**response.data)
            return None
        except Exception as e:
            print(f"❌ [AuthService.get_user_profile] Erreur: {e}")
            return None

    async def sign_out(self):
        """Déconnecte l'utilisateur actuel."""
        try:
            self.client.auth.sign_out()
        except Exception as e:
            print(f"❌ [AuthService.sign_out] Erreur: {e}")