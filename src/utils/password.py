# VRIED: The students used the scrypt library for hashing of passwords. For some reason this completely borked AES
# because apple sucks.
# I replaced this code to cryptography.

import os
import uuid
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey

def hash_password(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    return kdf.derive(password.encode('utf-8'))

def generate_salt() -> bytes:
    return os.urandom(16)

def verify_password(password: str, hashed_password: bytes, salt: bytes) -> bool:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    try:
        kdf.verify(password.encode('utf-8'), hashed_password)
        return True
    except InvalidKey:
        return False