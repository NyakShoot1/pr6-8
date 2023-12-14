from uuid import uuid4, UUID

import pytest

from app.models.task import Task, TaskStatuses
from app.repositories.bd_task_repo import TaskRepo


@pytest.fixture()
def task_repo() -> TaskRepo:
    repo = TaskRepo()
    return repo


@pytest.fixture()
def first_task() -> Task:
    return Task(id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"), title="Test", description="description",
                status=TaskStatuses.ACTIVATE, user_id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"))


@pytest.fixture()
def second_task() -> Task:
    return Task(id=uuid4(), title="Test", description="description",
                status=TaskStatuses.ACTIVATE, user_id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"))


def test_empty_list(task_repo: TaskRepo) -> None:
    assert task_repo.get_tasks() == []


def test_add_task(task_repo: TaskRepo, first_task: Task) -> None:
    task_repo.create_task(first_task)
    tasks = task_repo.get_tasks()
    assert len(tasks) == 1
    assert tasks[0] == first_task


def test_add_duplicate_task_error(task_repo: TaskRepo, first_task: Task) -> None:
    with pytest.raises(KeyError):
        task_repo.create_task(first_task)


def test_get_task_by_id(task_repo: TaskRepo, first_task: Task) -> None:
    retrieved_task = task_repo.get_task_by_id(first_task.id)
    assert retrieved_task == first_task


def test_done_task(task_repo: TaskRepo, first_task: Task) -> None:
    task_repo.done_task(first_task)
    tasks = task_repo.get_tasks()
    print(tasks[0].status)
    assert tasks[0].status == TaskStatuses.DONE


def test_get_task_by_id_error(task_repo: TaskRepo) -> None:
    with pytest.raises(KeyError):
        task_repo.get_task_by_id(uuid4())
