from fastapi import APIRouter 
import supabase 
from app.models.play import *
from app.core.database import supabase 
from datetime import datetime
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    play_data = {
            "id_user": play.id_user,
            "id_minigame": play.id_minigame,
            "score": play.score,
            "result": True,  # Asumiendo que 'True' significa éxito
            "money_earned": play.money_earned,
            #"played_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Mejor que "now()"
        }
    
    logger.info(f"Intentando insertar: {play_data}")
    
    response = supabase.table("minigames_results").insert(play_data).execute()
    
    return {
        "message": "Resultado creado exitosamente",
        "data": response.data
    }

#@router.put("/last_play/{id_user}/{id_minigame}")
#async def 