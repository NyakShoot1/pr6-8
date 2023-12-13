import traceback
import uuid
from uuid import UUID

import requests

from app.models.task import Task, TaskStatuses
from app.repositories.bd_task_repo import TaskRepo
from app.rabbitmq_produce import send_notification


class TaskService:
    task_repo: TaskRepo

    def __init__(self) -> None:
        self.task_repo = TaskRepo()

    def get_tasks(self) -> list[Task]:
        return self.task_repo.get_tasks()

    def create_task(self, title: str, description: str, user_id: UUID):
        # response = requests.get(f"http://127.0.0.1:8001/api/user/{user_id}")

        # if response.status_code == 200:
        new_task = Task(id=uuid.uuid4(), title=title, description=description, user_id=user_id,
                            status=TaskStatuses.ACTIVATE)
        send_notification(new_task)
        return self.task_repo.create_task(new_task)
        # else:
        #     raise KeyError

    def done_task(self, task_id: UUID) -> Task:
        task = self.task_repo.get_task_by_id(task_id)

        if task.status == TaskStatuses.DONE:
            raise ValueError

        task.status = TaskStatuses.DONE
        send_notification(task)
        return self.task_repo.done_task(task)
