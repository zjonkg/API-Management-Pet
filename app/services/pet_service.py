from app.core.database import supabase
from app.models.pet import Pet

def create_pet(pet: Pet):
    response = supabase.table("pets").insert(pet.model_dump()).execute()
    return response.data

def get_pet(pet_id: str):
    response = supabase.table("pets").select("*").eq("id", pet_id).execute()
    print(f"DB Response: {response.data}")  # Log para depuración
    if response.data:
        return response.data[0]
    return None

def update_pet_qr(pet_id: str, qr_code: str):
    try:
        # Llamar a la función SQL 'update_pet_qr_by_id' en PostgreSQL desde Supabase
        response = supabase.rpc('update_pet_qr_by_id', {"pet_id_input": pet_id, "qr_code_input": qr_code}).execute()
        
        # Verificar la respuesta
        print (response)
        
    except Exception as e:
        print(f"❌ Error al actualizar el QR: {e}")

def delete_pet(pet_id: str):
        
    response = (
        supabase.table("pets")
        .delete()
        .eq("id", pet_id)
        .execute()
    )

    print(response)

