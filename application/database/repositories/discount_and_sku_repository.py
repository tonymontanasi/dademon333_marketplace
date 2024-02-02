from uuid import UUID

from sqlalchemy import select

from application.database.models.discount_and_sku import (
    DiscountAndSKU,
    UpdateDiscountAndSKU,
)
from application.database.orm_models import DiscountAndSKUORM
from application.database.repositories.base_repository import BaseDbRepository


class DiscountAndSKURepository(
    BaseDbRepository[DiscountAndSKU, UpdateDiscountAndSKU, DiscountAndSKUORM]
):
    _model = DiscountAndSKU
    _table = DiscountAndSKUORM

    async def get_by_discount_id(
        self, discount_id: UUID
    ) -> list[DiscountAndSKU]:
        rows = await self.db_session.scalars(
            select(DiscountAndSKUORM).where(
                DiscountAndSKUORM.discount_id == discount_id
            )
        )
        return [DiscountAndSKU.model_validate(x) for x in rows.all()]

    async def get_by_sku_id(self, sku_id: UUID) -> list[DiscountAndSKU]:
        rows = await self.db_session.scalars(
            select(DiscountAndSKUORM).where(DiscountAndSKUORM.sku_id == sku_id)
        )
        return [DiscountAndSKU.model_validate(x) for x in rows.all()]
