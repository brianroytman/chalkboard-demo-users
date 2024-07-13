from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreateModel
from models import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        return await self.user_repository.create(session, new_user)