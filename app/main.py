from fastapi import FastAPI
from app.api.routes import pet
from app.api.routes import db
from app.api.routes import user
from app.api.routes import employees
from app.api.routes import achievements
from app.api.routes import ranking
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen (cambiar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir cualquier encabezado
)

app.include_router(pet.router, prefix="/pets", tags=["Pets"])
app.include_router(user.router, prefix="/user", tags=["Users"])  # Ruta original
app.include_router(db.router, prefix="/ds", tags=["Database"])  # Nueva ruta
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
app.include_router(ranking.router, prefix="/ranking", tags=["Ranking"])

@app.get("/")
def home():
    return {"message": "QR API for pets with Supabase"}
