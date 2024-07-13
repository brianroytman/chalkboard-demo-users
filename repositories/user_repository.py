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