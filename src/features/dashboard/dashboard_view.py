# src/features/dashboard/dashboard_view.py
import flet as ft

class DashboardView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Icon(icon=ft.Icons.LEADERBOARD, size=48, color=ft.Colors.GREEN_ACCENT),
                ft.Text("Classement Général", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Le tableau des scores des meilleurs pronostiqueurs s'affichera ici.", color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.expand = True
        self.alignment = ft.Alignment.CENTER