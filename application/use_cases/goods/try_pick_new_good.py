import logging

from application.database.models.good import Good
from application.database.models.posting_good import PostingGood
from application.database.models.task import Task, TaskType
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.sku_repository import SKURepository
from application.database.repositories.task_repository import TaskRepository
from application.utils.cost import fetch_good_cost

logger = logging.getLogger(__name__)


class TryPickNewGoodUseCase:
    def __init__(
        self,
        sku_repository: SKURepository,
        good_repository: GoodRepository,
        task_repository: TaskRepository,
        discount_repository: DiscountRepository,
        posting_good_repository: PostingGoodRepository,
    ):
        self.sku_repository = sku_repository
        self.good_repository = good_repository
        self.task_repository = task_repository
        self.discount_repository = discount_repository
        self.posting_good_repository = posting_good_repository

    async def execute(self, posting_good: PostingGood) -> Good | None:
        new_good = await self.good_repository.pick_available_by_sku(
            sku_id=posting_good.sku_id,
            stock=posting_good.stock,
        )
        if not new_good:
            logger.info("Нет доступного нового товара")
            return

        cost = await fetch_good_cost(
            good=new_good,
            sku_repository=self.sku_repository,
            discount_repository=self.discount_repository,
        )
        logger.info(f"Подобран новый товар {new_good.id} по цене {cost}")

        await self.posting_good_repository.create(
            PostingGood(
                posting_id=posting_good.posting_id,
                sku_id=posting_good.sku_id,
                good_id=new_good.id,
                good_stock=new_good.stock,
                cost=cost,
            )
        )
        logger.info(f"Добавили новый товар {new_good.id} к заказу")

        await self.task_repository.create(
            Task(
                type=TaskType.picking,
                sku_id=new_good.sku_id,
                stock=new_good.stock,
                count=1,
                posting_id=posting_good.posting_id,
                good_id=new_good.id,
            )
        )
        logger.info("Создали новую picking-задачу")
