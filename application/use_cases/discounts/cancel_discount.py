import logging

from application.database.models.discount import UpdateDiscount, DiscountStatus
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.use_cases.discounts.dto.cancel_discount import (
    CancelDiscountInputDTO,
)
from application.use_cases.discounts.exceptions import DiscountNotFound

logger = logging.getLogger(__name__)


class CancelDiscountUseCase:
    def __init__(self, discount_repository: DiscountRepository):
        self.discount_repository = discount_repository

    async def execute(self, input_dto: CancelDiscountInputDTO) -> None:
        logger.info(f"Закрытие скидки {input_dto.id}")

        discount = await self.discount_repository.get_by_id(input_dto.id)
        if not discount:
            logger.warning("Скидка не найдена в бд")
            raise DiscountNotFound()
        logger.info("Скидка найдена в бд")

        await self.discount_repository.update(
            UpdateDiscount(id=input_dto.id, status=DiscountStatus.finished)
        )
        logger.info("Закрыли скидку в бд")
