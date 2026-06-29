# src/main.py
import flet as ft
from features.auth.views.login_view import LoginView
from features.auth.state.auth_state import AuthState
from navigation.main_shell import MainShell


async def main(page: ft.Page):
    page.title = "Foot Preds - Arena"
    page.theme_mode = ft.ThemeMode.DARK

    # Configuration des dimensions minimales pour le comportement responsive
    page.window_min_width = 360
    page.window_min_height = 600

    auth_state = AuthState(page)

    async def navigate_to_dashboard():
        page.controls.clear()

        # Initialisation du Shell principal avec injection du callback de déconnexion
        shell = MainShell(page, on_logout=handle_logout)

        # Configuration des barres globales sur la page
        page.appbar = shell.appbar
        page.navigation_bar = shell.navigation_bar
        page.add(shell.main_content_container)
        page.update()

    async def handle_logout():
        from features.auth.data.auth_service import AuthService
        # Nettoyage à la fois sur le serveur Supabase et en session Flet
        await AuthService().sign_out()
        auth_state.clear_session()

        # Retrait des barres globales pour l'écran de login
        page.appbar = None
        page.navigation_bar = None
        await show_login()

    async def show_login():
        page.controls.clear()
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        login_screen = LoginView(page, on_login_success=navigate_to_dashboard)
        page.add(login_screen)
        page.update()

    # Routage initial au lancement
    if auth_state.is_authenticated:
        await navigate_to_dashboard()
    else:
        await show_login()


if __name__ == "__main__":
    ft.run(main)