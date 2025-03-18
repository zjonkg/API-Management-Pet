from pydantic import BaseModel
from typing import Optional
import uuid

class Pet(BaseModel):
    id: str = str(uuid.uuid4())  # Unique ID
    name: str
    type: str
    age: int
    qr_code: Optional[str] = None  # Permite que sea null
