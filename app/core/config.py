import os
import asyncpg
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Obtener las credenciales
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificar si las credenciales están correctamente cargadas
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Error: Las credenciales de Supabase no están configuradas correctamente en Railway o el entorno local")

print("✅ Variables de entorno cargadas correctamente.")

async def connect_db():
    return await asyncpg.connect(SUPABASE_URL)
