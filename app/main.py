from fastapi import FastAPI
from app.api.routes import pet
from app.api.routes import db
from app.api.routes import user
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

@app.get("/")
def home():
    return {"message": "QR API for pets with Supabase"}
