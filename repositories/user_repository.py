from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timezone
from fastapi import HTTPException, status


class UserRepository:
    async def create(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        return user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User:
        statement = select(User).filter(User.id == user_id)
        result = await session.execute(statement)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    async def get_all(self, session: AsyncSession) -> list[User]:
        statement = select(User).order_by(User.id)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def update(self, session: AsyncSession, user_id: int, data: dict) -> User:
        statement = select(User).filter(User.id == user_id)
        result = await session.execute(statement)
        try:
            user = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        for key, value in data.items():
            setattr(user, key, value)
        user.date_updated = datetime.now(timezone.utc)
        await session.commit()
        return user
    
    async def delete(self, session: AsyncSession, user_id: int) -> None:
        statement = select(User).filter(User.id == user_id)
        result = await session.execute(statement)
        try:
            user = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        await session.delete(user)
        await session.commit()