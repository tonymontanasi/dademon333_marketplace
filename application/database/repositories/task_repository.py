from uuid import UUID

from sqlalchemy import select

from application.database.models.task import Task, UpdateTask
from application.database.orm_models import TaskORM
from application.database.repositories.base_repository import BaseDbRepository


class TaskRepository(BaseDbRepository[Task, UpdateTask, TaskORM]):
    _model = Task
    _table = TaskORM

    async def get_by_acceptance_id(self, acceptance_id: UUID) -> list[Task]:
        result = await self.db_session.scalars(
            select(TaskORM).where(TaskORM.acceptance_id == acceptance_id)
        )
        return [Task.model_validate(x) for x in result.all()]
