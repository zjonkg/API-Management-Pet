from fastapi import APIRouter, HTTPException, status
import supabase
from app.models.users import *
from app.core.database import supabase
from app.services.supabase_service import test_db_connection
from app.services.hashed_password import hash_password
from app.services.token import create_access_token
from datetime import datetime, timedelta, timezone

router = APIRouter()

# Obtener todos los usuarios de la BBDD
@router.get("/")
async def get_users():
    response = supabase.table("users").select("*").execute()
    for user in response.data:
        del user["password"]
    return response.data

# Obtener un usuario por ID
@router.get("/{id}")
async def get_user(id: int):
    response = supabase.table("users").select("*").eq("id", id).execute()
    del response.data[0]["password"]
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

@router.get("/{id}/{token}")
async def access_token(id: int, token: str):
    """
    Verifica el token de acceso del usuario.
    
    Parámetros:
    - id: Id de usuario
    - token: Token de acceso
    """
    response = supabase.table("users").select("*").eq("id", id).eq("token_access", token).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Token no válido")
    
    return {"message": "Token válido"}

# Crear usuario
@router.post("/singup")
async def create_user(user: UserAll):
    """
    Crea un nuevo usuario.
    - **pet**: Información del usuario a crear.
    """
    user_data = user.dict()
    user_data["password"] = hash_password(user_data["password"])
    token = create_access_token(user_data)
    user_data["token_access"] = token

    response = supabase.table("users").insert(user_data).execute()
    #token_response = supabase.table("users_token").insert(token).execute()

    return {
        "message": "Usuario creado exitosamente",
        "token": token
        }

# Loging de usuario
@router.post("/login")
async def login(user: LoginRequest):

    response = supabase.table("users").select("*").eq("email", user.email).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    user_data = response.data[0]  
 
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
    "id": response.data[0]["id"],
    "has_mascot": response.data[0]["has_mascot"]}


@router.post("/achievements/{username}/{achievement_id}")
async def award_achievement(user: str, achievement_id: int):
    response_achievements = supabase.table("achievements").select("id, reward_coins").eq("id", achievement_id).execute()
    response_user = supabase.table("users").select("id, balance, day_streak, created_at").eq("username", user).execute()

    new_coins = response_achievements.data[0]["reward_coins"] + response_user.data[0]["balance"]

    insert_coins = supabase.table("users").update({
        "balance": new_coins,
    }).eq("username", user).execute()

    insert_responses = supabase.table("user_achievements").insert({
        "id_user": response_user.data[0]["id"],
        "id_achievement": response_achievements.data[0]["id"]
    }).execute()

    return {"message": "Logro añadido correctamente"}

@router.put("/last_conection/{id}")
async def last_conection(user: int):
    """
    Actualiza la fecha de la última conexión del usuario.
    
    Parámetros:
    - id: Id de usuario
    """
    response = supabase.table("users").update({"last_conection": "now()"}).eq("id", user).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": "Última conexión actualizada exitosamente"}

@router.put("/day_streak/{id}")
async def set_day_streak(user: int):
    response = supabase.table("users").select("day_streak, last_conection").eq("id", user).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_streak = response.data[0]
    last_conection = user_streak["last_conection"]

    try:
        if isinstance(last_conection, (int, float)):
            user_time = datetime.fromtimestamp(last_conection, timezone.utc)
        elif isinstance(last_conection, str):
            user_time = datetime.fromisoformat(last_conection) 
            if user_time.tzinfo is None:
                user_time = user_time.replace(tzinfo=timezone.utc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al parsear la fecha: {e}")

    time_now = datetime.now(timezone.utc)
    time_diff = time_now - user_time

    # Lógica de racha
    if time_diff <= timedelta(hours=24):
        new_streak = user_streak["day_streak"] + 1
    else:
        new_streak = 1

    update_response = supabase.table("users").update({
        "day_streak": new_streak,
        "last_conection": time_now.isoformat()
    }).eq("id", user).execute()
    
    return {"message": f"Racha actualizada a {new_streak} días"}

@router.put("/forgot-password")
async def forgot_password(email: str, user_data: ForgotPassword):
    """
    Cambia la contraseña de un usuario olvidada.
    
    Parámetros:
    - email: Correo electrónico del usuario (como query parameter)
    - new_password: Nueva contraseña
    - confirm_password: Confirmación de la nueva contraseña
    """
    if user_data.new_password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )
    
    try:
        user_response = supabase.table("users")\
                              .select("id")\
                              .eq("email", email)\
                              .execute()
        
        if not user_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe una cuenta con este correo electrónico"
            )
        
        # Actualizar contraseña
        update_response = supabase.table("users")\
                                .update({
                                    "password": hash_password(user_data.new_password),
                                    "updated_at": "now()"
                                })\
                                .eq("email", email)\
                                .execute()
        
        if not update_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo actualizar la contraseña"
            )
            
        return {"detail": "Contraseña actualizada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.put("/{id}")
async def update_user(id: str, user: UserAll):
    response = supabase.table("users").update(user).eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data[0]

@router.put("/update_balance/{id}/{coins}")
async def update_balance(id: int, coins: int):
    response = supabase.table("users").select("balance").eq("id", id).execute()

    new_value = response.data[0]["balance"] + coins

    supabase.table("users").update({"balance": new_value}).eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return {"message": "Balance updated successfully"}

@router.delete("/{id}")
async def delete_user(id: str):
    response = supabase.table("users").delete().eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data

@router.delete("/delete/token/{id}")
async def delete_token(id: str):
    response = supabase.table("users").update({"token_access": None}).eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data