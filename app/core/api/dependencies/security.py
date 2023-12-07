import bcrypt


def hash_password(password: str, salt_key: str):
    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt_key.encode("utf-8"))
    return hash_password


def checkPassword(password: bytes, hash_password: bytes):
    return bcrypt.checkpw(password, hash_password)
