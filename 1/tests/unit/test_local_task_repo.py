import pytest
from uuid import uuid4
from app.models.task import Task, TaskStatuses
from app.repositories.local_task_repo import TaskRepo


@pytest.fixture()
def task_repo() -> TaskRepo:
    return TaskRepo()


@pytest.fixture()
def example_task() -> Task:
    return Task(
        id=uuid4(),
        title='Example Task',
        description='Task description',
        status=TaskStatuses.ACTIVATE,
        user_id=uuid4()
    )


def test_get_tasks_empty(task_repo: TaskRepo):
    tasks = task_repo.get_tasks()
    assert len(tasks) == 0


def test_create_task(task_repo: TaskRepo, example_task: Task):
    created_task = task_repo.create_task(example_task)
    assert created_task in task_repo.get_tasks()


def test_create_duplicate_task_error(task_repo: TaskRepo, example_task: Task):
    task_repo.create_task(example_task)
    with pytest.raises(KeyError):
        task_repo.create_task(example_task)


def test_done_task(task_repo: TaskRepo, example_task: Task):
    created_task = task_repo.create_task(example_task)
    updated_task = task_repo.done_task(created_task)
    assert updated_task.status == TaskStatuses.DONE
    assert updated_task in task_repo.get_tasks()


def test_get_task_by_id(task_repo: TaskRepo, example_task: Task):
    created_task = task_repo.create_task(example_task)
    retrieved_task = task_repo.get_task_by_id(created_task.id)
    assert retrieved_task == created_task


def test_get_task_by_id_error(task_repo: TaskRepo):
    with pytest.raises(KeyError):
        task_repo.get_task_by_id(uuid4())
