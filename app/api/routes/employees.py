from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
import supabase
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models.employees import *
from app.core.database import supabase
from app.services.supabase_service import test_db_connection
from app.services.hashed_password import hash_password, verify_password

router = APIRouter()
security = HTTPBasic()

@router.get("/")
async def get_employees():
    response = supabase.table("employees").select("*").execute()
    return response.data

@router.get("/{id}")
async def get_employees(id: int):
    response = supabase.table("employees").select("*").eq("id", id).execute()
    return response.data

# registros
@router.post("/singup")
async def create_employee(employee: EmployeeAll):
    """
    Crea un nuevo empleado.
    - **employee**: Información del empleado a crear.
    """
    employee_data = employee.dict()
    employee_data["password"] = hash_password(employee_data["password"])

    response = supabase.table("employees").insert(employee_data).execute()
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Error creating employee")
    return response.json()

# login
@router.post("/login")
async def login(email: str, password: str):
    response = supabase.table("employees").select("password").eq("email", email).execute()

    if verify_password(password, response):
        return {"message": "Login successful"}