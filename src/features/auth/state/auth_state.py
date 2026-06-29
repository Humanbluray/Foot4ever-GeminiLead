# src/features/auth/state/auth_state.py
import flet as ft
from typing import Optional
from src.features.auth.data.models import UserProfile


class AuthState:
    """Gère l'état de l'utilisateur en utilisant la nouvelle API de stockage Flet."""

    def __init__(self, page: ft.Page):
        self.page = page

    @property
    def current_user(self) -> Optional[UserProfile]:
        # Utilisation de l'API mise à jour pour récupérer les données de session
        user_data = self.page.session.store.get("current_user")
        if user_data:
            return UserProfile(**user_data)
        return None

    @current_user.setter
    def current_user(self, user: Optional[UserProfile]):
        if user:
            # On stocke sous forme de dictionnaire (JSON ordonnable)
            self.page.session.store.set("current_user", user.model_dump())
        else:
            self.page.session.store.remove("current_user")

    def clear_session(self):
        self.page.session.store.clear()

    @property
    def is_authenticated(self) -> bool:
        return self.page.session.store.contains_key("current_user")

    @property
    def is_admin(self) -> bool:
        user = self.current_user
        return user is not None and user.is_admin