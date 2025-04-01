from fastapi import APIRouter, HTTPException, status
import supabase
from app.models.users import *
from app.services.supabase_service import test_db_connection

router = APIRouter()

@router.get("/users")
async def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/users/{id}")
async def get_user(id: str):
    response = supabase.table("users").select("*").eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

@router.post("/user")
async def create_user(user: UserAll):
    """
    Crea un nuevo usuario.
    - **pet**: Información del usuario a crear.
    """
    response = supabase.table("users").insert(user).execute()
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Error creating user")
    return response.data[0]

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


@router.put("/user/{email}/forgot_password", 
           status_code=status.HTTP_200_OK,
           responses={
               200: {"description": "Contraseña cambiada exitosamente"},
               400: {"description": "Las contraseñas no coinciden o el usuario no existe"},
               500: {"description": "Error del servidor al actualizar la contraseña"}
           })
async def forgot_password(email: str, user: ForgotPassword):
    """
    Cambia la contraseña de un usuario olvidada.
    
    - **email**: Correo electrónico del usuario (en path y body para doble verificación)
    - **new_password**: Nueva contraseña
    - **confirm_password**: Confirmación de la nueva contraseña (debe coincidir)
    """

    if email != user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo en la URL no coincide con el del cuerpo"
        )

    if user.new_password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )
    
    try:
        user_exists = supabase.table("users")\
                             .select("email")\
                             .eq("email", email)\
                             .execute()
        
        if not user_exists.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no existe"
            )

        response = supabase.table("users")\
                          .update({"password": user.new_password})\
                          .eq("email", email)\
                          .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo actualizar la contraseña"
            )
            
        return {"detail": "Contraseña cambiada exitosamente"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error del servidor: {str(e)}"
        )

@router.put("/user/{id}")
async def update_user(id: str, user: dict):
    response = supabase.table("users").update(user).eq("id", id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error updating user")
    return response.data[0]

@router.delete("/user/{id}")
async def delete_user(id: str):
    response = supabase.table("users").delete().eq("id", id).execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error deleting user")
    return {"detail": "User deleted successfully"}