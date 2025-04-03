import asyncio
import json
import os
from dotenv import load_dotenv
from supabase import acreate_client, AClient

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")
TABLE = "user_notificactions"

# Make sure to await the async creation of the client
async def main():
    while True:
        try:
            # Crear el cliente de supabase
            supabase: AClient = await acreate_client(SUPABASE_URL, SUPABASE_ANON_KEY)

            def my_callback(payload):
                print("Mensaje recibido:", payload)
                try:
                    # Validación de payload
                    if isinstance(payload, dict):
                        print("Datos del payload:", json.dumps(payload, indent=2))
                    else:
                        print("Payload no es un diccionario:", payload)
                except Exception as e:
                    print(f"Error al procesar el mensaje: {e}")

            # Establecer la conexión en realtime
            await supabase.realtime.connect()

            # Configuración de la suscripción y escuchando cambios
            await (supabase.realtime
                .channel("my_channel")
                .on_postgres_changes("INSERT", schema="public", table=TABLE, callback=my_callback)
                .subscribe())

            # Empezar a escuchar eventos
            await supabase.realtime.listen()

        except Exception as e:
            print(f"Error en la conexión o al procesar los mensajes: {e}")
            print("Intentando reconectar en 5 segundos...")
            await asyncio.sleep(5)  # Esperar 5 segundos antes de intentar reconectar

# Ejecutar la función principal
if __name__ == "__main__":
    asyncio.run(main())
