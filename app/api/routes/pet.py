from fastapi import APIRouter, HTTPException
from app.services.pet_service import create_pet, get_pet, delete_pet, assign_pet
from app.services.qr_service import validate_qr
from app.models.pet import Pet
from app.models.assign_pet_request import AssignPetRequest

router = APIRouter()

@router.post("/create")
def create(pet: Pet):
    return create_pet(pet)

@router.get("/get/{pet_id}")
def get(pet_id: str):
    return get_pet(pet_id)

@router.post("/assign_pet")
def assign(request: AssignPetRequest):
    return assign_pet(request)

@router.post("/validate_qr")
def validate_qr_code(content: str):
    return validate_qr(content)

@router.delete("/delete/{pet_id}")
def delete(pet_id: str):
    return delete_pet(pet_id)
