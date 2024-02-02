import logging
from uuid import UUID

from application.database.repositories.discount_and_sku_repository import (
    DiscountAndSKURepository,
)
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.use_cases.discounts.dto.get_discount import (
    GetDiscountOutputDTO,
)
from application.use_cases.discounts.exceptions import DiscountNotFound

logger = logging.getLogger(__name__)


class GetDiscountUseCase:
    def __init__(
        self,
        discount_repository: DiscountRepository,
        discount_and_sku_repository: DiscountAndSKURepository,
    ):
        self.discount_repository = discount_repository
        self.discount_and_sku_repository = discount_and_sku_repository

    async def execute(self, discount_id: UUID) -> GetDiscountOutputDTO:
        logger.info(f"Получение информации о акции {discount_id}")

        discount = await self.discount_repository.get_by_id(discount_id)
        if not discount:
            logger.warning("Акция не найдена")
            raise DiscountNotFound()
        logger.info("Акция найдена")

        sku_ids = await self.discount_and_sku_repository.get_by_discount_id(
            discount_id
        )
        logger.info(f"Найдено {len(sku_ids)} SKU")

        return GetDiscountOutputDTO(
            id=discount.id,
            status=discount.status,
            created_at=discount.created_at,
            percentage=discount.percentage,
            sku_ids=[x.sku_id for x in sku_ids],
        )
