import logging
from uuid import UUID

from application.database.models.posting import PostingStatus, UpdatePosting
from application.database.models.task import TaskStatus, TaskType, Task
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.posting_repository import (
    PostingRepository,
)
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.postings.dto.cancel_posting import (
    CancelPostingInputDTO,
)
from application.use_cases.postings.exceptions import (
    PostingNotFound,
    CantClosePosting,
)

logger = logging.getLogger(__name__)


class CancelPostingUseCase:
    def __init__(
        self,
        good_repository: GoodRepository,
        task_repository: TaskRepository,
        posting_repository: PostingRepository,
        posting_good_repository: PostingGoodRepository,
    ):
        self.good_repository = good_repository
        self.task_repository = task_repository
        self.posting_repository = posting_repository
        self.posting_good_repository = posting_good_repository

    async def execute(self, input_dto: CancelPostingInputDTO) -> None:
        posting_id = input_dto.id
        logger.info(f"Отмена заказа {posting_id}")

        posting = await self.posting_repository.get_by_id(posting_id)
        if not posting:
            logger.warning("Заказ не найден")
            raise PostingNotFound()
        logger.info("Заказ найден")

        if posting.status != PostingStatus.in_item_pick:
            logger.warning(
                f"Нельзя отменить заказ со статусом {posting.status}"
            )
            raise CantClosePosting()

        await self.posting_repository.update(
            UpdatePosting(id=posting_id, status=PostingStatus.canceled)
        )
        logger.info("Обновили статус заказа")

        await self.close_picking_tasks(posting_id)
        logger.info("Закрыли задачи на сбор")

        await self.create_placing_tasks(posting_id)
        logger.info("Создали задачи на размещение товаров на склад")

    async def close_picking_tasks(self, posting_id: UUID) -> None:
        tasks = await self.task_repository.get_by_posting_id(posting_id)
        logger.info(f"Найдено {len(tasks)} задач")

        await self.task_repository.update_status_by_ids(
            ids=[
                task.id
                for task in tasks
                if task.status == TaskStatus.in_work
                and task.type == TaskType.picking
            ],
            status=TaskStatus.canceled,
        )

    async def create_placing_tasks(self, posting_id: UUID) -> None:
        goods = await self.posting_good_repository.get_by_posting_id(
            posting_id
        )
        logger.info("Найдено {len(goods)} групп товаров в заказе")

        await self.task_repository.bulk_create(
            [
                Task(
                    type=TaskType.placing,
                    sku_id=good.sku_id,
                    stock=good.good_stock,
                    count=1,
                    posting_id=posting_id,
                    good_id=good.good_id,
                )
                for good in goods
                if not good.cancel_reason
            ]
        )
