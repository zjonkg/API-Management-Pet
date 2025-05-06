from pydantic import BaseModel

class Role(BaseModel):
    role_name: str
    description: str
    permission: str
