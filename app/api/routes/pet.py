from fastapi import APIRouter, HTTPException
from app.services.pet_service import create_pet, get_pet, update_pet_qr, delete_pet
from app.services.qr_service import generate_qr, validate_qr
from app.models.pet import Pet

router = APIRouter()


@router.post("/create")
def create(pet: Pet):
    created_pet = create_pet(pet)

    if not created_pet or "error" in created_pet:
        raise HTTPException(status_code=400, detail="Error al crear la mascota")
    
    pet_id = created_pet[0]["id"]  
    qr_code = generate_qr(pet_id)  
    update_pet_qr(pet_id, qr_code)  
    pet.qr_code = qr_code

    return {"pet": created_pet, "qr_code": f"data:image/png;base64,{qr_code}"}

@router.get("/get/{pet_id}")
def get(pet_id: str):
    pet = get_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.post("/validate_qr")
def validate_qr_code(content: str):
    """
    Valida si código QR de mascota es válido
    """
    result = validate_qr(content)
    
    return result

@router.post("/delete/{pet_id}")
def get(pet_id: str):
    pet = delete_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

