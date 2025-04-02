from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo
from typing import Optional

class Employee(BaseModel):
    name: str
    first_surname: str
    email: EmailStr
    phone_number: str
    role: int

class EmployeeAll(Employee):
    second_name: str
    second_surname: str
    birthdate: str
    address: str