import logging

from application.database.models.good import UpdateGood, GoodStock, Good
from application.database.models.posting_good import (
    PostingGoodCancelReason,
    UpdatePostingGood,
)
from application.database.models.task import TaskStatus
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.goods.dto.move_to_not_found import (
    MoveToNotFoundInputDTO,
)
from application.use_cases.goods.exceptions import GoodNotFound
from application.use_cases.goods.try_pick_new_good import TryPickNewGoodUseCase

logger = logging.getLogger(__name__)


class MoveToNotFoundUseCase:
    def __init__(
        self,
        good_repository: GoodRepository,
        task_repository: TaskRepository,
        posting_good_repository: PostingGoodRepository,
        picking_use_case: TryPickNewGoodUseCase,
    ):
        self.good_repository = good_repository
        self.task_repository = task_repository
        self.posting_good_repository = posting_good_repository
        self.picking_use_case = picking_use_case

    async def execute(self, input_dto: MoveToNotFoundInputDTO) -> None:
        good_id = input_dto.id
        logger.info(f"Переносим товар {good_id} на сток not_found")

        good = await self.good_repository.get_by_id(good_id)
        if not good or good.is_sold or good.stock == GoodStock.not_found:
            logger.warning("Товар или не найден, или продан, или утерян")
            raise GoodNotFound()

        await self.good_repository.update(
            UpdateGood(
                id=good_id, stock=GoodStock.not_found, is_reserved=False
            )
        )
        logger.info("Обновили stock и is_reserved")

        await self.update_posting_goods(good)
        logger.info("Обновили информацию о товаре в заказах")

    async def update_posting_goods(self, good: Good) -> None:
        posting_goods = await self.posting_good_repository.get_by_good_id(
            good.id
        )
        logger.info(
            f"Найдено {len(posting_goods)} упоминаний товара в posting_good"
        )

        for posting_good in posting_goods:
            if posting_good.cancel_reason:
                continue

            await self.posting_good_repository.update(
                UpdatePostingGood(
                    id=posting_good.id,
                    cancel_reason=PostingGoodCancelReason.not_found,
                )
            )
            logger.info(f"Удалили товар из заказа {posting_good.posting_id}")

            await self.picking_use_case.execute(posting_good)

    async def update_tasks(self, good: Good) -> None:
        tasks = await self.task_repository.get_by_good_id(good.id)
        logger.info(f"Нашли {len(tasks)} задач")

        to_close = [
            task.id for task in tasks if task.status == TaskStatus.in_work
        ]
        await self.task_repository.update_status_by_ids(
            ids=to_close, status=TaskStatus.canceled
        )
        logger.info(f"Закрыли {len(to_close)} задач")
