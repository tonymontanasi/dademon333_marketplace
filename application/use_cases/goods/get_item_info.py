import logging
from uuid import UUID

from application.database.repositories.good_repository import GoodRepository
from application.use_cases.goods.dto.get_item_info import GetItemInfoOutputDTO
from application.use_cases.goods.exceptions import GoodNotFound

logger = logging.getLogger(__name__)


class GetItemInfoUseCase:
    def __init__(
        self,
        good_repository: GoodRepository,
    ):
        self.good_repository = good_repository

    async def execute(self, good_id: UUID) -> GetItemInfoOutputDTO:
        logger.info(f"Получение информации о товаре {good_id}")

        good = await self.good_repository.get_by_id(good_id)
        if not good:
            logger.warning("Товар не найден")
            raise GoodNotFound()
        logger.info("Товар найден")

        return GetItemInfoOutputDTO(
            id=good.id,
            sku_id=good.sku_id,
            stock=good.stock,
            reserved_state=good.is_reserved,
        )
