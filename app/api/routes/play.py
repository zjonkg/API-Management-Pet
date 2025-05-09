from fastapi import APIRouter, HTTPException
import supabase
from app.models.play import *
from app.core.database import supabase

router = APIRouter()

@router.get("/")
async def get_result():
    response = supabase.table("minigames_results").select("*").execute()
    
    return response.data

@router.post("/")
async def create_result(play: Play):
    """
    Crea un nuevo resultado de minijuego.
    - **play**: Información del resultado a crear.
    """
    play_data = play.dict()
    
    response = supabase.table("minigames_result").insert(play_data).execute()
    
    return {
        "message": "Resultado creado exitosamente",
        "data": response.data
    }

#@router.put("/last_play/{id_user}/{id_minigame}")
#async def 