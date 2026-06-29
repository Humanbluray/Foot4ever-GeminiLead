# src/main.py
import flet as ft
from features.auth.state.auth_state import AuthState
from features.auth.views.login_view import LoginView


async def main(page: ft.Page):
    page.title = "Foot Preds - Arena"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    auth_state = AuthState(page)

    async def navigate_to_dashboard():
        page.controls.clear()
        user = auth_state.current_user
        welcome_message = f"Bienvenue, {user.username} !" if user else "Bienvenue !"
        role_badge = "🛡️ Espace Admin" if auth_state.is_admin else "⚽ Espace Joueur"

        page.add(
            ft.Column(
                controls=[
                    ft.Icon(icon=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                    ft.Text(welcome_message, size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(role_badge, size=16, color=ft.Colors.GREEN_ACCENT),
                    ft.ElevatedButton("Déconnexion", on_click=handle_logout)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()  # Nouvelle syntaxe épurée (update() est nativement async si dans main async)

    async def handle_logout(e):
        from features.auth.data.auth_service import AuthService
        await AuthService().sign_out()
        auth_state.clear_session()
        await show_login()

    async def show_login():
        page.controls.clear()
        login_screen = LoginView(page, on_login_success=navigate_to_dashboard)
        page.add(login_screen)
        page.update()

    # Initialisation
    if auth_state.is_authenticated:
        await navigate_to_dashboard()
    else:
        await show_login()


if __name__ == "__main__":
    # Remplacement officiel de ft.app() par ft.run()
    ft.run(main)
