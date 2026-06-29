# src/navigation/main_shell.py
import flet as ft
from src.features.auth.state.auth_state import AuthState
from navigation.routes import AppRoutes

# Import des vues
from src.features.dashboard.dashboard_view import DashboardView
from src.features.predictions.predictions_view import PredictionsView
from src.features.admin.admin_view import AdminView


class MainShell(ft.View):
    """
    Le Shell principal de l'application post-connexion.
    Gère la structure globale (AppBar, NavigationBar) et le switch d'écrans.
    """

    def __init__(self, page: ft.Page, on_logout):
        super().__init__()
        self.current_page = page
        self.on_logout = on_logout
        self.auth_state = AuthState(page)

        # Dictionnaire des vues instanciées pour éviter de les recréer à chaque clic
        self.views_cache = {
            AppRoutes.DASHBOARD: DashboardView(),
            AppRoutes.PREDICTIONS: PredictionsView(),
            AppRoutes.ADMIN: AdminView(),
        }

        # Si l'utilisateur est admin, on injecte la vue admin dans le cache
        if self.auth_state.is_admin:
            self.views_cache[AppRoutes.ADMIN] = AdminView()

        # Zone d'affichage centrale dynamique
        self.main_content_container = ft.Container(
            content=self.views_cache[AppRoutes.DASHBOARD],  # Vue par défaut
            expand=True,
            padding=15
        )

        # 1. Barre supérieure (AppBar)
        self.appbar = ft.AppBar(
            title=ft.Text(f"Arena • {self.auth_state.current_user.username if self.auth_state.current_user else ''}",
                          size=18, weight=ft.FontWeight.W_600),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            center_title=False,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT_ROUNDED,
                    icon_color=ft.Colors.RED_ACCENT,
                    tooltip="Se déconnecter",
                    on_click=self.handle_logout_click
                )
            ]
        )

        # 2. Barre de navigation inférieure (NavigationBar)
        nav_destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.LEADERBOARD, label="Classement"),
            ft.NavigationBarDestination(icon=ft.Icons.SPORTS_SOCCER, label="Pronos"),
        ]

        # Ajout conditionnel sécurisé de l'onglet admin selon le rôle en session
        if self.auth_state.is_admin:
            nav_destinations.append(
                ft.NavigationBarDestination(icon=ft.Icons.ADMIN_PANEL_SETTINGS, label="Admin")
            )

        self.navigation_bar = ft.NavigationBar(
            destinations=nav_destinations,
            selected_index=0,
            on_change=self.handle_navigation_change,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

        # Structure finale du Shell
        self.controls = [
            self.main_content_container
        ]

    def handle_navigation_change(self, e):
        """Permute le contenu central selon l'onglet cliqué."""
        index = int(e.data)

        # Cartographie des index vers nos routes
        routes_mapping = [AppRoutes.DASHBOARD, AppRoutes.PREDICTIONS]
        if self.auth_state.is_admin:
            routes_mapping.append(AppRoutes.ADMIN)

        target_route = routes_mapping[index]

        # Mise à jour du conteneur central avec la vue issue du cache
        self.main_content_container.content = self.views_cache[target_route]
        self.current_page.update()

    async def handle_logout_click(self, e):
        await self.on_logout()

