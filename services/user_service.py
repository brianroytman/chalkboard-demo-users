from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreateModel, UserUpdateModel
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

    async def get_user(self, user_id: int, session: AsyncSession) -> User:
        return await self.user_repository.get_by_id(session, user_id)

    async def get_users(self, session: AsyncSession) -> list[User]:
        return await self.user_repository.get_all(session)

    async def update_user(self, user_id: int, user_data: UserUpdateModel, session: AsyncSession) -> User:
        return await self.user_repository.update(session, user_id, user_data.model_dump())

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        return await self.user_repository.delete(session, user_id)
