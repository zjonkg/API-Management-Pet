from app.core.database import supabase

def test_db_connection():
    """Prueba la conexión a la base de datos obteniendo un solo registro de la tabla 'pets'."""
    try:
        response = supabase.table("pets").select("*").limit(1).execute()
        return {"status": "success", "message": "Database connection is working!", "sample_data": response.data}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
    
