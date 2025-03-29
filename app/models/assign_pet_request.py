from pydantic import BaseModel
from typing import Optional

class AssignPetRequest(BaseModel):
    qr_code: str
    user_id: str