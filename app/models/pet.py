from pydantic import BaseModel
from typing import Optional
import uuid


# Modelo para la solicitud (Request)
class PetCreateRequest(BaseModel):
    name: str
    id_pet_type: int
    id_user: Optional[int] = None  

# Modelo para la respuesta (Response)
class PetResponse(BaseModel):
    id: int
    name: str
    id_pet_type: int
    qr: Optional[str] = None 
    id_user: Optional[int] = None
    created_at: str


