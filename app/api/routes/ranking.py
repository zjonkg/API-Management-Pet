from fastapi import APIRouter
import supabase
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

@router.get("/most_achievements")
async def get_monst_achievements():
    """
    Get the user with the most achievements.
    """
    response_ranking = supabase.table("ranking").select("*").order("num_achievements", desc=True).execute()
    user_ids = [rank["id_user"] for rank in response_ranking.data]

    response_users = supabase.table("users").select("id, username").in_("id", user_ids).execute()
    users_dict = {user["id"]: user["username"] for user in response_users.data}

    ranking_data = []
    for rank in response_ranking.data:
        ranking_data.append({
            "id_user": rank["id_user"],
            "username": users_dict.get(rank["id_user"], "Usuario desconocido"),
            "num_achievements": rank["num_achievements"],
        })

    return ranking_data

@router.get("/most_days")
async def get_most_days():
    """
    Get the user with the most days.
    """
    response_ranking = supabase.table("ranking").select("*").order("days", desc=True).execute()
    user_ids = [rank["id_user"] for rank in response_ranking.data]

    response_users = supabase.table("users").select("id, username").in_("id", user_ids).execute()
    users_dict = {user["id"]: user["username"] for user in response_users.data}

    ranking_data = []
    for rank in response_ranking.data:
        ranking_data.append({
            "id_user": rank["id_user"],
            "username": users_dict.get(rank["id_user"], "Usuario desconocido"),
            "days": rank["days"],
        })

    return ranking_data

@router.post("/")
async def set_ranking_achievements(username: str, id_achievements: int):
    """
    Set ranking by achievements.
    """
    response_user = supabase.table("users").select("id, day_streak, created_at").eq("username", username).execute()
    response_achievements = supabase.table("user_achievements").select("*").eq("id_user", id_achievements).execute()

    response = supabase.table("ranking").insert({
        "id_user": response_user.data[0]["id"],
        "num_achievements": len(response_achievements.data),
        "time": response_user.data[0]["created_at"],
        "days": response_user.data[0]["day_streak"]
    }).execute()

    return {"message": "Añadido correctamente"}

@router.put("/")
async def update_ranking_achievements(username: str, id_achievements: int):
    """
    Update ranking by achievements.
    """
    response_user = supabase.table("users").select("id, day_streak, created_at").eq("username", username).execute()
    response_achievements = supabase.table("user_achievements").select("*").eq("id_user", id_achievements).execute()

    

    response = supabase.table("ranking").update({
        "num_achievements": len(response_achievements.data),
        "days": response_user.data[0]["day_streak"]
    }).eq("id_user", response_user.data[0]["id"]).execute()

    return {"message": "Actualizado correctamente"}