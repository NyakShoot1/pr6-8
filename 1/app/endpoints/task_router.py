from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.models.task import Task
from app.services.task_service import TaskService

task_router = APIRouter(prefix='/task', tags=['Task'])


@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService)) -> list[Task]:
    return task_service.get_tasks()


@task_router.post('/{id}/done')
def done_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.done_task(id)
        return task
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be done')
