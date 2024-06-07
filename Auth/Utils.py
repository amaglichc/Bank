import bcrypt


def generate_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_pw = password.encode("utf-8")
    return bcrypt.hashpw(password=bytes_pw, salt=salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password)
