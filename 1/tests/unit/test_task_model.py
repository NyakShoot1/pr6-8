import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.models.task import Task, TaskStatuses


@pytest.fixture()
def any_task() -> Task:
    return Task(
        id=uuid4(),
        title='Test Task',
        description='Task description',
        status=TaskStatuses.ACTIVATE,
        user_id=uuid4()
    )


def test_task_creation(any_task: Task):
    assert dict(any_task) == {
        'id': any_task.id,
        'title': any_task.title,
        'description': any_task.description,
        'status': any_task.status,
        'user_id': any_task.user_id
    }


def test_task_invalid_status(any_task: Task):
    with pytest.raises(ValidationError):
        Task(
            id=uuid4(),
            title='Test Task',
            description='Task description',
            status='invalid_status',
            user_id=uuid4()
        )
