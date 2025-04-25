from jose import jwt
import secrets
import base64

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, secrets.token_urlsafe(64), algorithm="HS256")

    return encoded_jwt