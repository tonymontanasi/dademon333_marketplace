from application.database.models.task import Task, UpdateTask
from application.database.orm_models import TaskORM
from application.database.repositories.base_repository import BaseDbRepository


class TaskRepository(BaseDbRepository[Task, UpdateTask, TaskORM]):
    _model = Task
    _table = TaskORM
