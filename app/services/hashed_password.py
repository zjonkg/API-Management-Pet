import bcrypt

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def verify_password(password, hashed_password):
    plain_password = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    if bcrypt.checkpw(hashed_bytes, hashed_password):
        return True