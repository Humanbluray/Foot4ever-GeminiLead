# src/features/admin/data/admin_service.py
from typing import List
from supabase import Client
from src.core.database.supabase_client import get_supabase
from src.features.admin.data.models import SeasonModel, CompetitionModel, GameWeekModel


class AdminService:
    def __init__(self):
        self.client: Client = get_supabase()

    # --- SAISONS ---
    def create_season(self, name: str) -> SeasonModel:
        data = {"name": name, "status": "À venir"}
        response = self.client.table("seasons").insert(data).execute()
        return SeasonModel(**response.data[0])

    async def get_all_seasons(self) -> List[SeasonModel]:
        response = self.client.table("seasons").select("*").order("created_at", desc=True).execute()
        return [SeasonModel(**item) for item in response.data]

    # --- COMPÉTITIONS ---
    def create_competition(self, season_id: int, name: str) -> CompetitionModel:
        """Insère une compétition liée à une saison."""
        data = {"season_id": season_id, "name": name, "status": "À venir"}
        response = self.client.table("competitions").insert(data).execute()
        return CompetitionModel(**response.data[0])

    def get_competitions_by_season(self, season_id: int) -> List[CompetitionModel]:
        """Récupère les compétitions d'une saison spécifique."""
        response = self.client.table("competitions").select("*").eq("season_id", season_id).order("name").execute()
        return [CompetitionModel(**item) for item in response.data]

    # --- GAMEWEEKS ---
    def create_gameweek(self, competition_id: int, title: str, closing_at_iso: str) -> GameWeekModel:
        """Insère une journée associée à une compétition."""
        data = {
            "competition_id": competition_id,
            "title": title,
            "closing_at": closing_at_iso,
            "status": "À venir"
        }
        response = self.client.table("gameweeks").insert(data).execute()
        return GameWeekModel(**response.data[0])