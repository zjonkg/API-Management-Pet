from fastapi import HTTPException
from app.core.database import supabase
from app.services.qr_service import generate_qr


def create_pet(pet):
    """Crea una nueva mascota en la base de datos y le asigna un QR."""
    
    created_pet_response = supabase.table("virtual_pets").insert(pet.dict(exclude_unset=True)).execute()

    if not created_pet_response.data:
        raise HTTPException(status_code=400, detail="Error al crear la mascota")
    
    pet_id = created_pet_response.data[0]["id"]  
    qr_code = generate_qr(pet_id)
    update_pet_qr(pet_id, qr_code)
    
    created_pet_response.data[0]["qr"] = qr_code

    return {"pet": created_pet_response.data[0]}

def get_pet(pet_id):
    """Obtiene una mascota por su ID."""
    response = supabase.table("virtual_pets").select("*").eq("id", pet_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Pet not found")

    return response.data[0]

def get_pets():
    """Obtiene una mascota por su ID."""
    response = supabase.table("virtual_pets").select("*").execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Pet not found")

    return response.data

def get_pet_by_qr(qr_code):
    """Obtiene una mascota por su código QR."""
    response = supabase.table("virtual_pets").select("*").eq("qr", qr_code).execute()

    if not response.data:
        return None  # No lanzar error aquí, lo manejamos en `assign_pet`
    
    return response.data[0]

def update_pet_qr(pet_id: str, qr_code: str):
    try:
        # Llamar a la función SQL 'update_pet_qr_by_id' en PostgreSQL desde Supabase
        response = supabase.rpc('update_pet_qr_by_id', {"pet_id_input": pet_id, "qr_code_input": qr_code}).execute()
        
        # Verificar la respuesta
        print (response)
        
    except Exception as e:
        print(f"❌ Error al actualizar el QR: {e}")

def assign_pet(request):
    """Asigna una mascota a un usuario si aún no tiene dueño."""
    pet = get_pet_by_qr(request.qr_code)

    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    if pet["id_user"] is not None:
        raise HTTPException(status_code=400, detail="Mascota ya tiene un dueño")

    response = supabase.table("virtual_pets").update({"id_user": request.user_id}).eq("id", pet["id"]).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Error al asignar la mascota")

    return {"message": "Mascota asignada correctamente", "pet": response.data[0]}

def delete_pet(pet_id):
    """Elimina una mascota de la base de datos."""
    pet = get_pet(pet_id)  # Verifica que existe antes de eliminar

    response = supabase.table("virtual_pets").delete().eq("id", pet_id).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Error al eliminar la mascota")

    return {"message": "Mascota eliminada correctamente"}
