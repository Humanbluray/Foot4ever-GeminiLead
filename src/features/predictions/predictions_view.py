# src/features/predictions/predictions_view.py
import flet as ft

class PredictionsView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Icon(ft.Icons.SPORTS_SOCCER, size=48, color=ft.Colors.GREEN_ACCENT),
                ft.Text("Mes Pronostics", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Grille des matchs de la Gameweek en cours.", color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.expand = True
        self.alignment = ft.Alignment.CENTER