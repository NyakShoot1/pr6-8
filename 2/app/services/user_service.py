import uuid
from uuid import UUID

from app.models.user import User
from app.repositories.local_user_repo import UserRepo


class UserService:
    user_repo: UserRepo

    def __init__(self) -> None:
        self.user_repo = UserRepo()

    def get_users(self) -> list[User]:
        return self.user_repo.get_users()

    def create_user(self, name: str, email: str):
        new_user = User(id=uuid.uuid4(), name=name, email=email)

        return self.user_repo.create_user(new_user)

    def get_user_by_id(self, user_id: UUID):
        return self.user_repo.get_user_by_id(user_id)

