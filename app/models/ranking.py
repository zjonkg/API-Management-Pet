from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo
from typing import Optional

class RankingAchievements(BaseModel):
    """
    Modelo para ranking de usuarios.
    """
    username: str
    id_achievements: int

class RankingTime(BaseModel):
    """
    Modelo para ranking por tiempo
    """
    username: str
    time: str

class RankingMoreDays(BaseModel):
    """
    Modelo para ranking por racha de dias
    """
    username: str
    days: str