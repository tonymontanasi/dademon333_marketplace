import logging
from uuid import UUID

from application.use_cases.tasks.dto.get_task_info import (
    GetTaskInfoOutputDTO,
    GetTaskInfoTargetOutputDTO,
)
from application.use_cases.tasks.exceptions import TaskNotFound

logger = logging.getLogger(__name__)


class GetTaskInfoUseCase:
    def __init__(self, task_repository):
        self.task_repository = task_repository

    async def execute(self, task_id: UUID) -> GetTaskInfoOutputDTO:
        logger.info(f"Получение информации о задаче {task_id}")

        task = await self.task_repository.get_by_id(task_id)
        if not task:
            logger.warning("Задача не найдена")
            raise TaskNotFound()
        logger.info("Задача найдена в бд")

        return GetTaskInfoOutputDTO(
            id=task.id,
            status=task.status,
            created_at=task.created_at,
            type=task.type,
            task_target=GetTaskInfoTargetOutputDTO(
                stock=task.stock,
                id=task.good_id if task.good_id else task.sku_id,
            ),
            posting_id=task.posting_id,
        )
