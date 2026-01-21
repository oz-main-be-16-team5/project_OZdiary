# app/services/user_service.py
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, hash_password
from app.models.user import UserModel


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def change_password(
        self, user: UserModel, current_password: str, new_password: str
    ) -> None:
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="current password is incorrect",
            )

        # 같은 비밀번호로 변경 방지(선택)
        if verify_password(new_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new password must be different",
            )

        new_hash = hash_password(new_password)
        await self.user_repo.update_password_hash(user, new_hash)
