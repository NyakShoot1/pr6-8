from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.services.user_service import UserService

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get('/')
def get_users(user_service: UserService = Depends(UserService)) -> list[User]:
    return user_service.get_users()


@user_router.get('/{user_id}')
def get_user_by_id(user_id: UUID, user_service: UserService = Depends(UserService)) -> User:
    return user_service.get_user_by_id(user_id)
