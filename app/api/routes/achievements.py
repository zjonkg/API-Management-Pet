from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
import supabase
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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