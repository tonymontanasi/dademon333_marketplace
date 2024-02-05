from uuid import UUID

from sqlalchemy import select, update

from application.database.models.task import Task, UpdateTask, TaskStatus
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

    async def get_by_posting_id(self, posting_id: UUID) -> list[Task]:
        result = await self.db_session.scalars(
            select(TaskORM).where(TaskORM.posting_id == posting_id)
        )
        return [Task.model_validate(x) for x in result.all()]

    async def update_status_by_ids(
        self, ids: list[UUID], status: TaskStatus
    ) -> None:
        await self.db_session.execute(
            update(TaskORM)
            .where(TaskORM.id.in_(ids))
            .values(status=status.value)
        )
