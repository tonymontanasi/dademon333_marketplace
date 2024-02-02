import logging
from uuid import UUID

from application.database.models.sku import SKU
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.sku_repository import SKURepository
from application.use_cases.sku.dto.get_sku_info import GetSKUInfoOutputDTO
from application.use_cases.sku.exceptions import SKUNotFound

logger = logging.getLogger(__name__)


class GetSKUInfoUseCase:
    def __init__(
        self,
        sku_repository: SKURepository,
        good_repository: GoodRepository,
        discount_repository: DiscountRepository,
    ):
        self.sku_repository = sku_repository
        self.good_repository = good_repository
        self.discount_repository = discount_repository

    async def execute(self, sku_id: UUID) -> GetSKUInfoOutputDTO:
        logger.info(f"Получение информации о SKU {sku_id}")

        sku = await self.sku_repository.get_by_id(sku_id)
        if not sku:
            logger.warning("SKU не найдена")
            raise SKUNotFound()
        logger.info("SKU найдена")

        actual_price = await self.get_actual_price(sku)
        logger.info(f"Текущая цена: {actual_price}")

        available_count = await self.good_repository.count_available_by_sku_id(
            sku_id
        )
        logger.info(f"На складе находится {available_count} единиц товара")

        return GetSKUInfoOutputDTO(
            id=sku.id,
            created_at=sku.created_at,
            actual_price=actual_price,
            base_price=sku.base_price,
            count=available_count,
            is_hidden=sku.is_hidden,
        )

    async def get_actual_price(self, sku: SKU) -> float:
        discounts = await self.discount_repository.get_actual_by_sku_id(sku.id)
        logger.info(f"Найдено {len(discounts)} активных скидок")
        if not discounts:
            return sku.base_price

        max_discount = max([x.percentage for x in discounts])
        return round(sku.base_price * (1 - max_discount / 100), 2)
