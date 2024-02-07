import logging
from uuid import UUID

from application.database.repositories.good_repository import GoodRepository
from application.use_cases.goods.dto.get_item_info_by_sku_id import (
    GetItemInfoBySKUIdOutputDTO,
    GetItemInfoBySKUIdItemOutputDTO,
)

logger = logging.getLogger(__name__)


class GetItemInfoBySKUIdUseCase:
    def __init__(self, good_repository: GoodRepository):
        self.good_repository = good_repository

    async def execute(self, sku_id: UUID) -> GetItemInfoBySKUIdOutputDTO:
        logger.info(f"Получение информации о товарах по SKU {sku_id}")

        goods = await self.good_repository.get_by_sku_id(sku_id)
        logger.info(f"Найдено {len(goods)} товаров")

        return GetItemInfoBySKUIdOutputDTO(
            items=[
                GetItemInfoBySKUIdItemOutputDTO(
                    item_id=item.id,
                    stock=item.stock,
                    reserved_state=item.is_reserved,
                )
                for item in goods
            ]
        )
