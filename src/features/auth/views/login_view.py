# src/features/auth/views/login_view.py
import flet as ft
from src.features.auth.data.auth_service import AuthService
from src.features.auth.state.auth_state import AuthState


class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        # Correction : On utilise un nom privé pour éviter le conflit avec la propriété native de Flet
        self.current_page = page
        self.on_login_success = on_login_success
        self.auth_service = AuthService()
        self.auth_state = AuthState(page)

        # Composants UI
        self.email_input = ft.TextField(
            label="Adresse Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.GREEN_ACCENT,
        )

        self.password_input = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.GREEN_ACCENT,
        )

        self.error_text = ft.Text(color=ft.Colors.RED_ACCENT, size=14, weight=ft.FontWeight.W_500)
        self.loading_indicator = ft.ProgressRing(width=24, height=24, visible=False, stroke_width=3,
                                                 color=ft.Colors.GREEN_ACCENT)

        self.login_button = ft.Button(
            content="Se connecter",
            style=ft.ButtonStyle(
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.GREEN_ACCENT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.handle_login,
            height=48,
        )

        # Layout
        self.content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCK_PERSON_OUTLINED, size=48, color=ft.Colors.GREEN_ACCENT),
                        ft.Text("Connexion Coach", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Entrez vos accès pour gérer vos pronos", size=14, color=ft.Colors.GREY_400),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        self.email_input,
                        self.password_input,
                        self.error_text,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row([self.login_button, self.loading_indicator],
                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
                width=400,
            ),
            elevation=4,
        )
        self.alignment = ft.Alignment.CENTER

    async def handle_login(self, e):
        self.error_text.value = ""
        self.login_button.disabled = True
        self.loading_indicator.visible = True
        self.current_page.update()  # Mis à jour avec self.current_page

        email = self.email_input.value.strip()
        password = self.password_input.value.strip()

        if not email or not password:
            self.error_text.value = "⚠️ Veuillez remplir tous les champs."
            self.login_button.disabled = False
            self.loading_indicator.visible = False
            self.current_page.update()
            return

        try:
            user_profile = await self.auth_service.sign_in(email, password)
            if user_profile:
                self.auth_state.current_user = user_profile
                await self.on_login_success()
            else:
                self.error_text.value = "❌ Identifiants invalides ou profil introuvable."
        except Exception:
            self.error_text.value = "❌ Erreur de connexion au serveur."
        finally:
            self.login_button.disabled = False
            self.loading_indicator.visible = False
            self.current_page.update()

