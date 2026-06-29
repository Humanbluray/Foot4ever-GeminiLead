import flet as ft
from flet.core.view import View
from styles import login_style
from utils import BG_COLOR, MAIN_COLOR, SECOND_COLOR
from components import MyButton


class LoginView(View):
    def __init__(self, page: ft.Page):
        super().__init__(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            route="/",
            spacing=0,
            bgcolor=BG_COLOR,
        )
        self.page = page

        # --- Champs de saisie avec mode adaptatif ---
        self.email = ft.TextField(
            **login_style,
            label="Email",
            prefix_icon=ft.Icons.MAIL_OUTLINE,
            adaptive=True,
        )
        self.password = ft.TextField(
            **login_style,
            label="Mot de passe",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            adaptive=True,
        )

        # --- Construction de la vue ---
        self.controls = [
            ft.SafeArea(
                content=ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                spacing=0,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(
                                                        "Foot",
                                                        size=24,
                                                        font_family="PEB",
                                                        color=MAIN_COLOR,
                                                    ),
                                                    ft.Text(
                                                        "4Ever",
                                                        size=24,
                                                        font_family="PEB",
                                                        color=SECOND_COLOR,
                                                    ),
                                                ],
                                            ),
                                            ft.Divider(height=2, color=ft.Colors.TRANSPARENT),
                                            self.email,
                                            self.password,
                                            MyButton("Se connecter", None),
                                        ],
                                        spacing=10,
                                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                    ),
                                    # Padding intérieur fixe (adapté à tous les écrans)
                                    padding=25,
                                    border_radius=10,
                                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                                    # Largeur gérée par ResponsiveRow
                                    col={
                                        "xs": 12,   # mobile : plein écran
                                        "sm": 10,
                                        "md": 8,
                                        "lg": 6,
                                        "xl": 5,
                                    },
                                ),
                            ],
                            run_spacing=10,
                        ),
                    ],
                )
            )
        ]