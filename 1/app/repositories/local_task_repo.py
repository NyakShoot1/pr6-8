from typing import List
from uuid import UUID

from app.models.task import Task, TaskStatuses

tasks: List[Task] = []


class TaskRepo:
    def get_tasks(self) -> list[Task]:
        return tasks

    def get_task_by_id(self, task_id: UUID) -> Task:
        for t in tasks:
            if t.id == task_id:
                return t

        raise KeyError

    def create_task(self, new_task: Task) -> Task:
        if len([t for t in tasks if t.id == new_task.id]) > 0:
            raise KeyError

        tasks.append(new_task)

        return new_task

    def done_task(self, task: Task) -> Task:
        for t in tasks:
            if t.id == task.id:
                t.status = task.status
                break

        return task
