# src/features/admin/data/admin_service.py
from typing import List
from supabase import Client
from src.core.database.supabase_client import get_supabase
from src.features.admin.data.models import SeasonModel, CompetitionModel, GameWeekModel, MatchModel

class AdminService:
    def __init__(self):
        self.client: Client = get_supabase()

    # --- SAISONS ---
    async def create_season(self, name: str) -> SeasonModel:
        data = {"name": name, "status": "À venir"}
        response = self.client.table("seasons").insert(data).execute()
        return SeasonModel(**response.data[0])

    async def get_all_seasons(self) -> List[SeasonModel]:
        response = self.client.table("seasons").select("*").order("created_at", desc=True).execute()
        return [SeasonModel(**item) for item in response.data]

    # --- COMPÉTITIONS ---
    async def create_competition(self, season_id: int, name: str) -> CompetitionModel:
        """Insère une compétition liée à une saison."""
        data = {"season_id": season_id, "name": name, "status": "À venir"}
        response = self.client.table("competitions").insert(data).execute()
        return CompetitionModel(**response.data[0])

    async def get_competitions_by_season(self, season_id: int) -> List[CompetitionModel]:
        """Récupère les compétitions d'une saison spécifique."""
        response = self.client.table("competitions").select("*").eq("season_id", season_id).order("name").execute()
        return [CompetitionModel(**item) for item in response.data]

    # --- GAMEWEEKS ---
    async def create_gameweek(self, competition_id: int, title: str, closing_at_iso: str) -> GameWeekModel:
        """Insère une journée associée à une compétition."""
        data = {
            "competition_id": competition_id,
            "title": title,
            "closing_at": closing_at_iso,
            "status": "À venir"
        }
        response = self.client.table("gameweeks").insert(data).execute()
        return GameWeekModel(**response.data[0])

    # --- AJOUTS POUR LES MATCHS (Fin de la classe AdminService) ---
    async def get_gameweeks_by_competition(self, competition_id: int) -> List[GameWeekModel]:
        """Récupère toutes les journées d'une compétition."""
        response = self.client.table("gameweeks").select("*").eq("competition_id", competition_id).order(
            "created_at").execute()
        return [GameWeekModel(**item) for item in response.data]

    async def create_match(self, gameweek_id: int, home: str, away: str, date_iso: str, match_type: str) -> MatchModel:
        """Insère un match lié à une journée."""
        data = {
            "gameweek_id": gameweek_id,
            "home_team": home,
            "away_team": away,
            "match_date": date_iso,
            "match_type": match_type
        }
        response = self.client.table("matches").insert(data).execute()
        return MatchModel(**response.data[0])