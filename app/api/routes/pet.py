from fastapi import APIRouter, HTTPException
from app.services.pet_service import create_pet, get_pet, delete_pet, assign_pet
from app.services.qr_service import validate_qr
from app.models.pet import PetCreateRequest
from app.models.pet import PetResponse
from app.models.assign_pet_request import AssignPetRequest

router = APIRouter()

@router.post("/create", summary="Crear una nueva mascota", description="Este endpoint crea una nueva mascota en el sistema")
def create(pet: PetCreateRequest):
    """
    Crea una nueva mascota.
    - **pet**: Información de la mascota a crear.
    """
    return create_pet(pet)

@router.get("/get/{pet_id}", summary="Obtener información de una mascota", description="Este endpoint obtiene la información de una mascota usando su ID", response_model=PetResponse)
def get(pet_id: str):
    """
    Obtiene la información de una mascota a través de su ID.
    - **pet_id**: El ID único de la mascota.
    """
    return get_pet(pet_id)

@router.post("/assign_pet", summary="Asignar una mascota a un dueño", description="Este endpoint asigna una mascota a un dueño")
def assign(request: AssignPetRequest):
    """
    Asigna una mascota a un dueño.
    - **request**: Información sobre la asignación (mascota y dueño).
    """
    return assign_pet(request)

@router.post("/validate_qr", summary="Validar un código QR", description="Este endpoint valida un código QR para obtener información relacionada con una mascota.")
def validate_qr_code(content: str):
    """
    Valida un código QR.
    - **content**: El contenido del código QR que se desea validar.
    """
    return validate_qr(content)

@router.delete("/delete/{pet_id}", summary="Eliminar una mascota", description="Este endpoint elimina una mascota del sistema usando su ID")
def delete(pet_id: str):
    """
    Elimina una mascota por su ID.
    - **pet_id**: El ID único de la mascota a eliminar.
    """
    return delete_pet(pet_id)
