from argon2 import PasswordHasher

argon = PasswordHasher()


def hash_passwd(raw_password: str | bytes) -> str | bytes:
    hashed = argon.hash(raw_password)
    return hashed


def verify_passwd(hashed: str | bytes, rawpswd: str | bytes) -> bool:
    try:
        result = argon.verify(hashed, rawpswd)
        return result
    except:
        return False
