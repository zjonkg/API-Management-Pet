import qrcode
import io
import base64
import hmac
import hashlib

SECRET_KEY = b"tilin123"

def generate_qr(data: str) -> str:
    """
    Genera un código QR con un HMAC para evitar exponer la clave secreta.
    """
    # Crear firma HMAC
    signature = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()
    qr_content = f"{data}:{signature}"

    # Generar QR
    qr = qrcode.make(qr_content)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def validate_qr(content: str) -> dict:
    """
    Valida un código QR verificando la firma HMAC.
    """
    try:
        data, received_signature = content.rsplit(":", 1)
        expected_signature = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_signature, expected_signature):
            return {"valid": True, "data": data}
        else:
            return {"valid": False, "message": "QR inválido"}
    except ValueError:
        return {"valid": False, "message": "Formato incorrecto"}
