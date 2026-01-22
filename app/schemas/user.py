from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):  # 회원가입
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):  # 로그인
    email: EmailStr
    password: str


class UserUpdate(BaseModel):  # 유저 이름,이메일 변경
    username: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None


class PasswordChange(BaseModel):  # 비밀번호 변경
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
