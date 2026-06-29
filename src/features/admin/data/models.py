# Mises à jour dans src/features/admin/data/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SeasonModel(BaseModel):
    id: Optional[int] = None
    name: str
    status: str = "À venir"
    created_at: Optional[datetime] = None

class CompetitionModel(BaseModel):
    id: Optional[int] = None
    season_id: int
    name: str
    status: str = "À venir"
    created_at: Optional[datetime] = None

class GameWeekModel(BaseModel):
    id: Optional[int] = None
    competition_id: int
    title: str
    status: str = "À venir"
    closing_at: datetime
    created_at: Optional[datetime] = None
