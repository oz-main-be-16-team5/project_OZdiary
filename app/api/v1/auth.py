from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    PasswordChange,
    UserResponse,
    TokenResponse,
    UserIdByTokenRequest,
    UserIdByTokenResponse,
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
        raise HTTPException(status_code=401, detail="인증 정보가 없습니다.")

    payload = decode_token(cred.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    user = await UserModel.filter(user_id=int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="비활성화된 사용자 입니다.")

    return user


# 회원가입
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(payload: UserCreate):
    """
    - 신규 사용자 회원가입
    - 이메일 중복 여부 확인
    - 비밀번호 해싱 후 사용자 저장
    """
    exists = await UserModel.filter(email=payload.email).exists()
    if exists:
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일 입니다.")

    pw_hash = hash_password(payload.password)

    user = await UserModel.create(
        username=payload.username,
        email=payload.email,
        password_hash=pw_hash,
        is_active=True,
    )

    return UserResponse(
        id=user.user_id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


# 로그인
@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    """
    - 사용자 로그인
    - username / password 검증
    - 인증 성공 시 토큰 발급
    """
    user = await UserModel.filter(email=payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="비활성화된 사용자 입니다."
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    token = create_access_token(subject=str(user.user_id))
    return TokenResponse(access_token=token, token_type="bearer")


# 조회
@router.get("/me", response_model=UserResponse)
async def me(user: UserModel = Depends(get_current_user)):
    """
    - 토큰 기반 사용자 정보 조회
    - 로그인된 사용자만 접근 가능
    """
    return UserResponse(
        id=user.user_id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


# 수정
@router.patch("/me", response_model=UserResponse)
async def update_me(payload: UserUpdate, user: UserModel = Depends(get_current_user)):
    """
    - 로그인한 사용자 정보 수정
    -  수정 가능 항목 : username,email
    """
    # 아무것도 안보내는거 방지
    if payload.username is None and payload.email is None:
        raise HTTPException(status_code=400, detail="수정할 항목이 없습니다.")

    if payload.email is not None and payload.email != user.email:
        exists = await UserModel.filter(email=payload.email).exists()
        if exists:
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일 입니다.")
        user.email = payload.email

    if payload.username is not None:
        user.username = payload.username

    await user.save()

    return UserResponse(
        id=user.user_id,
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
    """
    - 로그인된 사용자 비밀번호 변경
    - 기존 비밀번호 검증 후 변경
    """
    # 현재 비밀번호 확인
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(
            status_code=400, detail="현재 비밀번호가 올바르지 않습니다."
        )
    user.password_hash = hash_password(payload.new_password)
    await user.save(update_fields=["password_hash"])

    return None


@router.post("/extract-id", response_model=UserIdByTokenResponse)
async def get_user_id_by_token(payload: UserIdByTokenRequest):
    """
    JSON 바디로 전달된 토큰을 디코딩하여 user_id를 반환합니다.
    """
    try:
        # 1. 토큰 디코딩 (유효기간 및 서명 검증)
        decoded_payload = decode_token(payload.token)

        # 2. sub(user_id) 추출
        user_id = decoded_payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401, detail="토큰에 사용자 정보가 없습니다."
            )

        return UserIdByTokenResponse(user_id=user_id)

    except Exception as e:
        # 토큰이 만료되었거나 변조된 경우 decode_token에서 발생한 에러 처리
        raise HTTPException(
            status_code=401, detail=f"유효하지 않은 토큰 입니다.: {str(e)}"
        )
