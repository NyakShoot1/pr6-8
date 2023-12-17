# /app/repositories/bd_task_repo.py

import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import Task as DBTask


class TaskRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, task: DBTask) -> Task:
        result = dict(Task.model_validate(task))
        result = Task(id=result["id"], title=result["title"], description=result["description"], status=result["status"], user_id=result["user_id"])
        return result

    def _map_to_schema(self, task: Task) -> DBTask:
        data = dict(task)
        # del data['task']
        data['id'] = task.id if task != None else None
        result = DBTask(**data)

        return result

    def get_tasks(self) -> list[Task]:
        tasks = []
        for t in self.db.query(DBTask).all():
            tasks.append(t)
        return tasks

    def get_task_by_id(self, id: UUID) -> Task:
        task = self.db \
            .query(DBTask) \
            .filter(DBTask.id == id) \
            .first()
        task = self._map_to_model(task)
        if task == None:
            raise KeyError
        return task

    def create_task(self, task: Task) -> Task:
        try:
            db_task = self._map_to_schema(task)
            self.db.add(db_task)
            self.db.commit()
            return task
        except:
            traceback.print_exc()
            raise KeyError

    def done_task(self, task: Task) -> Task:
        db_task = self.db.query(DBTask).filter(
            DBTask.id == task.id).first()
        db_task.status = task.status
        self.db.commit()
        return self._map_to_model(db_task)
