import qrcode
import io
import base64
import hmac
import hashlib

SECRET_KEY = b"tilin123"

def generate_qr(data) -> str:
    """
    Genera un código QR con un HMAC para evitar exponer la clave secreta.
    """
    data_str = str(data)

    # Crear firma HMAC
    signature = hmac.new(SECRET_KEY, data_str.encode(), hashlib.sha256).hexdigest()
    qr_content = f"{data_str}:{signature}"

    qr = qrcode.make(qr_content)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return qr_content  



def validate_qr(content: str) -> dict:
    """
    Valida un código QR verificando la firma HMAC.
    """
    try:
        print(f"Contenido del QR: {content}")  # Para depuración
        data, received_signature = content.rsplit(":", 1)
        expected_signature = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_signature, expected_signature):
            return {"valid": True, "data": data}
        else:
            return {"valid": False, "message": "QR inválido"}
    except ValueError:
        return {"valid": False, "message": "Formato incorrecto"}
