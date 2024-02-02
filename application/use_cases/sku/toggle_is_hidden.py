import logging

from application.database.models.sku import UpdateSKU
from application.database.repositories.sku_repository import SKURepository
from application.use_cases.sku.dto.toggle_is_hidden import (
    ToggleIsHiddenInputDTO,
)
from application.use_cases.sku.exceptions import SKUNotFound

logger = logging.getLogger(__name__)


class ToggleIsHiddenUseCase:
    def __init__(self, sku_repository: SKURepository):
        self.sku_repository = sku_repository

    async def execute(self, input_dto: ToggleIsHiddenInputDTO) -> None:
        logger.info(
            f"Переключение is_hidden у SKU {input_dto.sku_id}"
            f" на {input_dto.is_hidden}"
        )

        sku = await self.sku_repository.get_by_id(input_dto.sku_id)
        if not sku:
            logger.warning("SKU не найдена")
            raise SKUNotFound()
        logger.info("SKU найдена")

        await self.sku_repository.update(
            UpdateSKU(id=sku.id, is_hidden=input_dto.is_hidden)
        )
        logger.info("Обновили видимость SKU")
