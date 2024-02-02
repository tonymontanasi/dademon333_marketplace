import logging

from application.database.models.discount import Discount
from application.database.models.discount_and_sku import DiscountAndSKU
from application.database.repositories.discount_and_sku_repository import (
    DiscountAndSKURepository,
)
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.sku_repository import SKURepository
from application.use_cases.discounts.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)
from application.use_cases.sku.exceptions import SKUNotFound

logger = logging.getLogger(__name__)


class CreateDiscountUseCase:
    def __init__(
        self,
        sku_repository: SKURepository,
        discount_repository: DiscountRepository,
        discount_and_sku_repository: DiscountAndSKURepository,
    ):
        self.sku_repository = sku_repository
        self.discount_repository = discount_repository
        self.discount_and_sku_repository = discount_and_sku_repository

    async def execute(
        self, input_dto: CreateDiscountInputDTO
    ) -> CreateDiscountOutputDTO:
        logger.info(f"Создание скидки на {len(input_dto.sku_ids)} ")

        skus = await self.sku_repository.get_by_ids(input_dto.sku_ids)
        if len(skus) != len(input_dto.sku_ids):
            logger.info(f"Найдено {len(skus)} из {len(input_dto.sku_ids)} SKU")
            raise SKUNotFound()
        logger.info("Все SKU найдены")

        discount = await self.discount_repository.create(
            Discount(percentage=input_dto.percentage)
        )
        logger.info(f"Создали скидку {discount.id}")

        await self.discount_and_sku_repository.bulk_create(
            [
                DiscountAndSKU(discount_id=discount.id, sku_id=sku_id)
                for sku_id in input_dto.sku_ids
            ]
        )
        logger.info("Прикрепили sku к скидке")

        return CreateDiscountOutputDTO(id=discount.id)
