from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session
from schemas import UserModel, UserCreateModel, UserUpdateModel
from services.user_service import UserService

router = APIRouter()

user_service = UserService()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        user = await user_service.create_user(user_data, session)
        return user
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    