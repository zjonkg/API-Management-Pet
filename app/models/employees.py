from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo
from typing import Optional

class Employee(BaseModel):
    name: str
    first_surname: str
    email: EmailStr
    password: str
    phone_number: str
    role: int

class EmployeeAll(Employee):
    second_name: str
    second_surname: str
    address: str

class LoginRequest(BaseModel):
    email: str
    password: str