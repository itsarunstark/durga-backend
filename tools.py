import hashlib

def encrypt(password:str)->str:
    return hashlib.sha256(password.encode()).hexdigest()