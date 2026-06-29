# src/features/admin/admin_view.py
import flet as ft
from src.features.admin.data.admin_service import AdminService
from datetime import datetime


class AdminView(ft.Container):
    def __init__(self):
        # Initialisation du Container parent sans logique lourde
        super().__init__()
        self.admin_service = AdminService()
        self.expand = True

        # --- BLOC SAISON ---
        self.season_name_input = ft.TextField(label="Nom de la Saison (ex: Édition 2026)", expand=True)
        self.season_submit_btn = ft.ElevatedButton("Créer Saison", on_click=self.handle_create_season,
                                                   bgcolor=ft.Colors.GREEN_ACCENT, color=ft.Colors.BLACK)

        # --- BLOC COMPÉTITION ---
        self.season_fp_dropdown = ft.Dropdown(label="Associer à la Saison", expand=True)
        self.comp_name_input = ft.TextField(label="Nom de la Compétition (ex: Elite One)", expand=True)
        self.comp_submit_btn = ft.ElevatedButton("Créer Compétition", on_click=self.handle_create_competition,
                                                 bgcolor=ft.Colors.ORANGE_ACCENT, color=ft.Colors.BLACK)

        # --- BLOC GAMEWEEK ---
        self.season_gw_dropdown = ft.Dropdown(label="1. Choisir Saison", expand=True, on_text_change=self.handle_season_gw_change)
        self.comp_gw_dropdown = ft.Dropdown(label="2. Choisir Compétition", expand=True, disabled=True)
        self.gw_title_input = ft.TextField(label="Titre de la Journée (ex: Journée 1)", expand=True)
        self.gw_closing_input = ft.TextField(label="Clôture (AAAA-MM-JJ HH:MM)",
                                             value=datetime.now().strftime("%Y-%m-%d 18:00"), expand=True)
        self.gw_submit_btn = ft.ElevatedButton("Créer Journée", on_click=self.handle_create_gameweek,
                                               bgcolor=ft.Colors.BLUE_ACCENT, color=ft.Colors.WHITE)

        self.status_text = ft.Text("", weight=ft.FontWeight.BOLD)

        # Assemblage de la vue dans le contrôle de contenu
        self.content = ft.ListView(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color=ft.Colors.RED_ACCENT, size=32),
                    ft.Text("Console d'Administration Pro", size=24, weight=ft.FontWeight.BOLD)
                ]),
                self.status_text,

                # CARD 1 : SAISONS
                ft.Card(content=ft.Container(content=ft.Column(
                    [ft.Text("🌱 Étape 1 : Créer une Saison", size=16, weight=ft.FontWeight.W_600),
                     ft.Row([self.season_name_input, self.season_submit_btn])]), padding=15)),

                # CARD 2 : COMPÉTITIONS
                ft.Card(content=ft.Container(content=ft.Column(
                    [ft.Text("🏆 Étape 2 : Créer une Compétition", size=16, weight=ft.FontWeight.W_600),
                     self.season_fp_dropdown, ft.Row([self.comp_name_input, self.comp_submit_btn])]), padding=15)),

                # CARD 3 : GAMEWEEKS
                ft.Card(content=ft.Container(content=ft.Column(
                    [ft.Text("📅 Étape 3 : Planifier les Journées", size=16, weight=ft.FontWeight.W_600),
                     ft.Row([self.season_gw_dropdown, self.comp_gw_dropdown]),
                     ft.Row([self.gw_title_input, self.gw_closing_input]),
                     ft.Row([self.gw_submit_btn], alignment=ft.MainAxisAlignment.END)]), padding=15)),
            ],
            spacing=15,
        )

    def did_mount(self):
        """
        Méthode de cycle de vie native de Flet.
        Exécutée automatiquement APPRÈS que l'affichage est monté et stable.
        """
        self.page.run_task(self._refresh_seasons)

    def show_message(self, text: str, is_error: bool = False):
        self.status_text.value = text
        self.status_text.color = ft.Colors.RED_ACCENT if is_error else ft.Colors.GREEN_ACCENT
        self.update()

    async def _refresh_seasons(self, e=None):
        """Récupère les saisons et remplit les menus déroulants de manière asynchrone."""
        try:
            seasons = await self.admin_service.get_all_seasons()
            options = [ft.dropdown.Option(key=str(s.id), text=s.name) for s in seasons]

            self.season_fp_dropdown.options = options
            self.season_gw_dropdown.options = options
            self.update()
        except Exception as ex:
            print(f"Erreur chargement saisons: {ex}")

    async def handle_create_season(self, e):
        name = self.season_name_input.value.strip()
        if not name: return

        self.season_submit_btn.disabled = True
        self.update()

        try:
            await self.admin_service.create_season(name)
            self.season_name_input.value = ""
            self.show_message(f"🎉 Saison '{name}' ajoutée.")
            await self._refresh_seasons()
        except Exception:
            self.show_message("❌ Erreur lors de la création.", is_error=True)
        finally:
            self.season_submit_btn.disabled = False
            self.update()

    async def handle_create_competition(self, e):
        season_id = self.season_fp_dropdown.value
        name = self.comp_name_input.value.strip()
        if not season_id or not name:
            self.show_message("⚠️ Sélectionne une saison et saisis un nom.", is_error=True)
            return

        self.comp_submit_btn.disabled = True
        self.update()

        try:
            await self.admin_service.create_competition(int(season_id), name)
            self.comp_name_input.value = ""
            self.show_message(f"🎉 Compétition '{name}' créée !")
        except Exception:
            self.show_message("❌ Erreur lors de la création.", is_error=True)
        finally:
            self.comp_submit_btn.disabled = False
            self.update()

    def handle_season_gw_change(self, e):
        """Déclenché quand l'admin choisit une saison dans le bloc Journée."""
        season_id = self.season_gw_dropdown.value
        if not season_id: return

        try:
            comps = self.admin_service.get_competitions_by_season(int(season_id))
            self.comp_gw_dropdown.options = [ft.dropdown.Option(key=str(c.id), text=c.name) for c in comps]
            self.comp_gw_dropdown.disabled = False
            self.update()

        except Exception as ex:
            print(f"Erreur chargement compétitions: {ex}")

    def handle_create_gameweek(self, e):
        comp_id = self.comp_gw_dropdown.value
        title = self.gw_title_input.value.strip()
        closing = self.gw_closing_input.value.strip()

        if not comp_id or not title or not closing:
            self.show_message("⚠️ Données incomplètes.", is_error=True)
            return

        try:
            datetime.strptime(closing, "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_message("❌ Format de date incorrect (AAAA-MM-JJ HH:MM).", is_error=True)
            return

        self.gw_submit_btn.disabled = True
        self.update()

        try:
            self.admin_service.create_gameweek(int(comp_id), title, closing)
            self.gw_title_input.value = ""
            self.show_message(f"🎉 {title} ajoutée avec succès !")
        except Exception:
            self.show_message("❌ Erreur lors de la création de la journée.", is_error=True)
        finally:
            self.gw_submit_btn.disabled = False
            self.update()