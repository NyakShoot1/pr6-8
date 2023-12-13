from typing import List
from uuid import UUID

from app.models.user import User

users: List[User] = []


class UserRepo:
    def get_users(self) -> list[User]:
        return users

    def get_user_by_id(self, user_id: UUID):
        for t in users:
            if t.id == user_id:
                return t

        raise KeyError

    def create_user(self, new_user: User) -> User:
        if len([t for t in users if t.id == new_user.id]) > 0:
            raise KeyError

        users.append(new_user)

        return new_user
