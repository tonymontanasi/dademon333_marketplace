import logging

from application.database.models.acceptance import Acceptance
from application.database.models.good import GoodStock
from application.database.models.sku import SKU
from application.database.models.task import Task, TaskType
from application.database.repositories.acceptance_repository import \
    AcceptanceRepository
from application.database.repositories.sku_repository import SKURepository
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.acceptances.dto.create_acceptance import \
    CreateAcceptanceInputDTO, CreateAcceptanceOutputDTO, \
    CreateAcceptanceItemInputDTO

logger = logging.getLogger(__name__)


class CreateAcceptanceUseCase:
    def __init__(
        self,
        acceptance_repository: AcceptanceRepository,
        sku_repository: SKURepository,
        task_repository: TaskRepository
    ):
        self.acceptance_repository = acceptance_repository
        self.task_repository = task_repository
        self.sku_repository = sku_repository

    async def execute(
        self,
        input_dto: CreateAcceptanceInputDTO
    ) -> CreateAcceptanceOutputDTO:
        acceptance = await self.acceptance_repository.create(Acceptance())
        logger.info(f"Создана приёмка {acceptance.id}")

        for item in input_dto.items_to_accept:
            await self.process_item(item, acceptance)

        return CreateAcceptanceOutputDTO(id=acceptance.id)

    async def process_item(
        self,
        item: CreateAcceptanceItemInputDTO,
        acceptance: Acceptance
    ) -> Task:
        logger.info(f"Обработка группы с id {item.sku_id}")

        sku = await self.sku_repository.get_by_id(item.sku_id)
        if not sku:
            sku = await self.sku_repository.create(SKU(id=item.sku_id))
            logger.info(f"Создана группа с id {item.sku_id}")
        else:
            logger.info(f"Найдена группа с id {item.sku_id}")

        task = await self.task_repository.create(
            Task(
                type=TaskType.placing,
                acceptance_id=acceptance.id,
                sku_id=sku.id,
                stock=GoodStock(item.stock),
                count=item.count
            )
        )
        logger.info(f"Создана задача на размещение {task.id}")
        return task
