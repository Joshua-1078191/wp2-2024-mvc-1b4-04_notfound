import os
import uuid

from scrypt import scrypt

def hash_password(password: str, salt: str) -> str:
    return scrypt.hash(password, salt)
    #return password + salt  # we don't currently have hashing implemented

def generate_salt() -> str:
    return str(uuid.uuid4())

def verify_password(password: str, hashed_password:str, salt: str) -> bool:
    return hashed_password == scrypt.hash(password, salt)
    #return hashed_password == hash_password(password, salt)