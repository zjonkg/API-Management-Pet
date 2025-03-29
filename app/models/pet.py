from pydantic import BaseModel
from typing import Optional
import uuid

class Pet(BaseModel):
    name: str
    id_pet_type: int
    id_user: Optional[int] = None
    qr: Optional[str] = None  # Permite que sea null
