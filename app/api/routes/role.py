from fastapi import APIRouter, HTTPException
import supabase
from app.models.role import *
from app.core.database import supabase

router = APIRouter()

# Obtener todos los roles de la BBDD
@router.get("/")
async def get_roles():
    response = supabase.table("role").select("*").execute()
    return response.data

@router.post("/")
async def create_role(role: Role):
    """
    Crea un nuevo rol.
    - **role**: Información del rol a crear.
    """
    role_data = role.dict()
    response = supabase.table("role").insert(role_data).execute()
    
    if response.data is None:
        raise HTTPException(status_code=400, detail="Error creating role")
    
    return response.data
