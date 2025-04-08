from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
import supabase
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models.employees import *
from app.core.database import supabase
from app.models.ranking import *

router = APIRouter()

@router.get("/")
async def get_all_ranking():
    """
    Get all rankings.
    """
    response = supabase.table("ranking").select("*").execute()
    return response.data

@router.post("/achievements")
async def set_ranking_achievements(ranking: RankingAchievements):
    """
    Set ranking by achievements.
    """
    response_user = supabase.table("users").select("username, created_at").eq("username", ranking.username).execute()
    response_achievements = supabase.table("user_achievements").select("*").eq("id_user", ranking.id_achievements).execute()