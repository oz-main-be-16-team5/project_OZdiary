from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer 토큰 꺼내기 (Authorization: Bearer xxx)
_bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    # bcrypt는 72 bytes 제한이 있어서 안전장치
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long (max 72 bytes for bcrypt)"
        )
    return _pwd.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return _pwd.verify(plain_password, password_hash)

async def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """
    Authorization 헤더에서 Bearer 토큰만 뽑아서 반환.
    - 없으면 401
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return credentials.credentials
