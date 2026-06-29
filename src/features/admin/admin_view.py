# src/features/admin/admin_view.py
import flet as ft

class AdminView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=48, color=ft.Colors.RED_ACCENT),
                ft.Text("Panneau d'Administration", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Gestion des saisons, clôture des journées et saisie des scores réels.", color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.expand = True
        self.alignment = ft.Alignment.CENTER