from fastapi import APIRouter, HTTPException
from app.services.supabase_service import test_db_connection

router = APIRouter()

@router.get("/test-dbs")
def test_database():
    """Endpoint para verificar la conexión con Supabase."""
    result = test_db_connection()

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result