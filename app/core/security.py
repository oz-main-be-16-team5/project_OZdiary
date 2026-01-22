from passlib.context import CryptContext
from fastapi import HTTPException

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long (max 72 bytes for bcrypt)"
        )
    return _pwd.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _pwd.verify(plain_password, password_hash)
