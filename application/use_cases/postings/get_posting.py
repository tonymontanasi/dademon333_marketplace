import logging
from collections import defaultdict
from uuid import UUID

from application.database.models.good import GoodStock
from application.database.models.posting_good import (
    PostingGood,
    PostingGoodCancelReason,
)
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.posting_repository import (
    PostingRepository,
)
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.postings.dto.get_posting import (
    GetPostingOutputDTO,
    GetPostingGoodOutputDTO,
    GetPostingTaskOutputDTO,
)
from application.use_cases.postings.exceptions import PostingNotFound

logger = logging.getLogger(__name__)


class GetPostingUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        posting_repository: PostingRepository,
        posting_good_repository: PostingGoodRepository,
    ):
        self.task_repository = task_repository
        self.posting_repository = posting_repository
        self.posting_good_repository = posting_good_repository

    async def execute(self, posting_id: UUID) -> GetPostingOutputDTO:
        logger.info(f"Получение информации о заказе {posting_id}")

        posting = await self.posting_repository.get_by_id(posting_id)
        if not posting:
            logger.warning("Заказ не найден")
            raise PostingNotFound()

        tasks = await self.task_repository.get_by_posting_id(posting_id)
        logger.info(f"Нашли {len(tasks)} задач")

        goods = await self.posting_good_repository.get_by_posting_id(
            posting_id
        )
        logger.info(f"Нашли {len(goods)} товаров по заказу")

        total_cost = self.get_total_cost(goods)
        logger.info(f"Итоговая стоимость заказа: {total_cost}")

        ordered_goods = self.get_ordered_goods(goods)
        logger.info(f"Получено {len(ordered_goods)} групп товаров в заказе")

        return GetPostingOutputDTO(
            id=posting.id,
            status=posting.status,
            created_at=posting.created_at,
            cost=total_cost,
            ordered_goods=ordered_goods,
            not_found=[
                good.good_id
                for good in goods
                if good.cancel_reason == PostingGoodCancelReason.not_found
            ],
            task_ids=[
                GetPostingTaskOutputDTO(
                    id=task.id, status=task.status, type=task.type
                )
                for task in tasks
            ],
        )

    @staticmethod
    def get_total_cost(goods: list[PostingGood]) -> float:
        total_cost = 0.0

        for good in goods:
            if good.cancel_reason:
                continue
            total_cost += good.cost

        return total_cost

    @staticmethod
    def get_ordered_goods(
        goods: list[PostingGood],
    ) -> list[GetPostingGoodOutputDTO]:
        goods_by_sku = defaultdict(list)

        for good in goods:
            if good.cancel_reason:
                continue
            goods_by_sku[good.sku_id].append(good)

        return [
            GetPostingGoodOutputDTO(
                sku=sku_id,
                from_valid_ids=[
                    good.good_id
                    for good in sku_goods
                    if good.stock == GoodStock.valid
                ],
                from_defect_ids=[
                    good.good_id
                    for good in sku_goods
                    if good.stock == GoodStock.defect
                ],
            )
            for sku_id, sku_goods in goods_by_sku.items()
        ]
