from fastapi import APIRouter, HTTPException
import supabase
from app.models.achievements import *
from app.core.database import supabase

router = APIRouter()

@router.get("/")
async def get_achievements():
    """
    Get all achievements
    """
    response = supabase.from_("achievements").select("*").execute()
    return response.data

@router.get("/{id}")
async def get_achievement(id: int):
    """
    Get achievement by id
    """
    response = supabase.from_("achievements").select("*").eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return response.data

@router.get("/user/{user_id}")
async def get_user_achievements(user_id: int):
    """
    Get achievements by user id
    """
    response = supabase.from_("user_achievements").select("*").eq("id_user", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Achievements not found")
    return response.data