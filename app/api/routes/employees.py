from fastapi import APIRouter, HTTPException
import supabase
from fastapi.security import HTTPBasic
from app.models.employees import *
from app.core.database import supabase
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

@router.post("/singup")
async def create_employee(employee: EmployeeAll):
    """
    Crea un nuevo empleado.
    - **employee**: Información del empleado a crear.
    """
    employee_data = employee.dict()
    employee_data["password"] = hash_password(employee_data["password"])

    response = supabase.table("employees").insert(employee_data).execute()
    if response.data is None:
        raise HTTPException(status_code=400, detail="Error creating employee")
    return response.data

@router.post("/login")
async def login(employee: LoginRequest):

    response = supabase.table("employees").select("*").eq("email", employee.email).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    employee_data = response.data[0]  
 
    if not verify_password(employee.password, employee_data["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}

