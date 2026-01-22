from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    PasswordChange,
    UserResponse,
    TokenResponse,
)
from app.models.user import UserModel
from app.core.security import hash_password, verify_password
from app.core.jwt import decode_token, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])

bearer = HTTPBearer(auto_error=False)


# 로그인을 한 유저인지 확인
async def get_current_user(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> UserModel:
    if cred is None or cred.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    payload = decode_token(cred.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = await UserModel.filter(id=int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


# 회원가입
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(payload: UserCreate):
    exists = await UserModel.filter(email=payload.email).exists()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")

    pw_hash = hash_password(payload.password)

    user = await UserModel.create(
        username=payload.username,
        email=payload.email,
        password_hash=pw_hash,
        is_active=True,
    )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


# 로그인
@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    user = await UserModel.filter(email=payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token, token_type="bearer")


# 조회
@router.get("/me", response_model=UserResponse)
async def me(user: UserModel = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
    )


# 수정
@router.patch("/me", response_model=UserResponse)
async def update_me(payload: UserUpdate, user: UserModel = Depends(get_current_user)):
    # 아무것도 안보내는거 방지
    if payload.username is None and payload.email is None:
        raise HTTPException(status_code=400, detail="No fields to update")

    if payload.email is not None and payload.email != user.email:
        exists = await UserModel.filter(email=payload.email).exists()
        if exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = payload.email

    if payload.username is not None:
        user.username = payload.username

    await user.save()

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


# 비밀번호 변경
@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: PasswordChange, user: UserModel = Depends(get_current_user)
):
    # 현재 비밀번호 확인
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user.password_hash = hash_password(payload.new_password)
    await user.save(update_fields=["password_hash"])

    return None
