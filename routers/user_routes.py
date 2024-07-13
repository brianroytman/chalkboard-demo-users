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
    
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await user_service.get_user(user_id, session)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    try:
        users = await user_service.get_users(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def update_user(user_id: int, user_data: UserUpdateModel, session: AsyncSession = Depends(get_session)):
    try:
        user = await user_service.update_user(user_id, user_data, session)
        return user
    except Exception as e:
        await session.rollback()  # Rollback in case of an error

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await user_service.delete_user(user_id, session)
        return {"message": "User deleted successfully"}
    except Exception as e:
        await session.rollback()  # Rollback in case of an error