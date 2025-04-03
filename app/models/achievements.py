from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo

class Achievement(BaseModel):
    name: str
    description: str
    rewars_coins: int
    rewards_item_id: int