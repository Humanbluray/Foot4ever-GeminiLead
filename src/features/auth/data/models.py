# src/features/auth/data/models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    username: str
    avatar_url: Optional[str] = None
    role: str = "player"  # 'player' ou 'admin'
    created_at: Optional[datetime] = None

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"