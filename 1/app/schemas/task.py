from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.task import TaskStatuses
from app.schemas.base_schema import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TaskStatuses]
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
