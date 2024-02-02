import logging
from uuid import UUID

from application.database.models.task import Task, TaskStatus
from application.database.repositories.acceptance_repository import (
    AcceptanceRepository,
)
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.acceptances.dto.get_acceptance_info import (
    GetAcceptanceInfoOutputDTO,
    GetAcceptanceInfoAcceptedItemOutputDTO,
    GetAcceptanceInfoTaskOutputDTO,
)
from application.use_cases.acceptances.exceptions import AcceptanceNotFound

logger = logging.getLogger(__name__)


class GetAcceptanceInfoUseCase:
    def __init__(
        self,
        acceptance_repository: AcceptanceRepository,
        task_repository: TaskRepository,
    ):
        self.acceptance_repository = acceptance_repository
        self.task_repository = task_repository

    async def execute(self, acceptance_id: UUID) -> GetAcceptanceInfoOutputDTO:
        logger.info(f"Получение информации о приёмке {acceptance_id}")

        acceptance = await self.acceptance_repository.get_by_id(acceptance_id)
        if not acceptance:
            logger.warning("Приёмка не найдена")
            raise AcceptanceNotFound()
        logger.info("Приёмка найдена в бд")

        tasks = await self.task_repository.get_by_acceptance_id(acceptance_id)
        logger.info(f"Найдено {len(tasks)} задач на приёмку")

        return GetAcceptanceInfoOutputDTO(
            id=acceptance.id,
            created_at=acceptance.created_at,
            accepted=self.get_accepted_items(tasks),
            task_ids=self.get_task_ids(tasks),
        )

    @staticmethod
    def get_accepted_items(
        tasks: list[Task],
    ) -> list[GetAcceptanceInfoAcceptedItemOutputDTO]:
        return [
            GetAcceptanceInfoAcceptedItemOutputDTO(
                sku_id=task.sku_id,
                stock=task.stock,
                count=task.count,
            )
            for task in tasks
            if task.status == TaskStatus.completed
        ]

    @staticmethod
    def get_task_ids(
        tasks: list[Task],
    ) -> list[GetAcceptanceInfoTaskOutputDTO]:
        return [
            GetAcceptanceInfoTaskOutputDTO(
                id=task.id,
                status=task.status,
            )
            for task in tasks
        ]
