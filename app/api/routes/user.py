from fastapi import APIRouter, HTTPException, status
import supabase
from app.models.users import *
from app.core.database import supabase
from app.services.supabase_service import test_db_connection
from app.services.hashed_password import hash_password

router = APIRouter()

@router.get("/")
async def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/{id}")
async def get_user(id: int):
    response = supabase.table("users").select("*").eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]


@router.post("/signup")
async def create_user(user: UserAll):
    """
    Crea un nuevo usuario.
    - **pet**: Información del usuario a crear.
    """

    user_data = user.dict()
    user_data["password"] = hash_password(user_data["password"])

    response = supabase.table("users").insert(user_data).execute()
    return response.data[0]

@router.post("/login2")
async def login(user: LoginRequest):

    response = supabase.table("users").select("*").eq("email", user.email).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    user_data = response.data[0]  
 
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}


@router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin):
    try:
        response = supabase.table("users").select("*").eq("email", user.email).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
            
        user_data = response.data[0]
        
        return user_data 
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el servidor: {str(e)}"
        )

@router.post("/achievements/{username}/{achievement_id}")
async def award_achievement(user: str, achievement_id: int):
    response_achievements = supabase.table("achievements").select("id").eq("id", achievement_id).execute()
    response_user = supabase.table("users").select("id").eq("username", user).execute()

    insert_responses = supabase.table("user_achievements").insert({
        "id_user": response_user.data[0]["id"],
        "id_achievement": response_achievements.data[0]["id"]
    }).execute()
    return insert_responses

@router.put(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Contraseña cambiada exitosamente"},
        400: {"description": "Las contraseñas no coinciden o el usuario no existe"},
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error del servidor al actualizar la contraseña"}
    }
)
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
async def update_user(id: str, user: dict):
    response = supabase.table("users").update(user).eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data[0]

@router.delete("/{id}")
async def delete_user(id: str):
    response = supabase.table("users").delete().eq("id", id).execute()
    if (response.count == None):
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data
