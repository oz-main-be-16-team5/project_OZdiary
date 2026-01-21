from app.models.user import UserModel


class UserRepository:
    async def get_by_email(self, email):
        return await UserModel.filter(email=email).first()

    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
    ):
        return await UserModel.create(
            username=username,
            email=email,
            password_hash=password_hash,
        )

    async def update_password_hash(self, user, password_hash):
        user.password_hash = password_hash
        await user.save()
