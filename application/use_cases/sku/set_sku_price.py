import logging

from application.database.models.sku import UpdateSKU
from application.database.repositories.sku_repository import SKURepository
from application.use_cases.sku.dto.set_sku_price import SetSKUPriceInputDTO
from application.use_cases.sku.exceptions import SKUNotFound

logger = logging.getLogger(__name__)


class SetSKUPriceUseCase:
    def __init__(self, sku_repository: SKURepository):
        self.sku_repository = sku_repository

    async def execute(self, input_dto: SetSKUPriceInputDTO) -> None:
        logger.info(
            f"Изменение цены у SKU {input_dto.sku_id}"
            f" на {input_dto.base_price}"
        )

        sku = await self.sku_repository.get_by_id(input_dto.sku_id)
        if not sku:
            logger.warning("SKU не найдена")
            raise SKUNotFound()
        logger.info("SKU найдена")

        await self.sku_repository.update(
            UpdateSKU(id=sku.id, base_price=input_dto.base_price)
        )
        logger.info("Обновили стоимость SKU")
