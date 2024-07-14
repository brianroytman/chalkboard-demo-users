from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
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
    except IntegrityError as e:
        await session.rollback()  # Rollback in case of an error
        if 'username' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        if 'email' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unique constraint violation")
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await user_service.get_user(user_id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
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
    except IntegrityError as e:
        await session.rollback()  # Rollback in case of an error
        if 'username' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        if 'email' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unique constraint violation")
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await user_service.delete_user(user_id, session)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

