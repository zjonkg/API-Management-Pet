from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    email: str 
    password: str

class UserAll(User):
    birthday: str | None = Field(None, alias="Birthday")
    phone_number: str

class ChangePassword():
    old_password: str
    new_password: str
    confirm_password:str

class ForgotPassword(BaseModel):
    """
    Modelo para el cambio de contraseña en caso de olvido.
    
    Campos requeridos:
    - new_password: Nueva contraseña (mínimo 8 caracteres)
    - confirm_password: Confirmación de la nueva contraseña
    """
    new_password: str = Field(..., min_length=8, max_length=64, 
                              description="Nueva contraseña (mínimo 8 caracteres)")
    confirm_password: str = Field(..., description="Confirmación de la nueva contraseña")

    @field_validator('new_password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(char.isupper() for char in v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError('Las contraseñas no coinciden')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    is_active: Optional[bool] = True
    
    class Config:
        # Esto asegura que aunque el modelo ORM tenga más campos, solo se devuelvan estos
        orm_mode = True