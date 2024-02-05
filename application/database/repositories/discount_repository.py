from uuid import UUID

from sqlalchemy import select, Join, and_

from application.database.models.discount import (
    Discount,
    UpdateDiscount,
    DiscountStatus,
)
from application.database.orm_models import DiscountORM, DiscountAndSKUORM
from application.database.repositories.base_repository import BaseDbRepository


class DiscountRepository(
    BaseDbRepository[Discount, UpdateDiscount, DiscountORM]
):
    _model = Discount
    _table = DiscountORM

    async def get_actual_by_sku_id(self, sku_id: UUID) -> list[Discount]:
        rows = await self.db_session.scalars(
            select(DiscountORM)
            .select_from(
                Join(
                    DiscountAndSKUORM,
                    DiscountORM,
                    DiscountAndSKUORM.discount_id == DiscountORM.id,
                    isouter=True,
                )
            )
            .where(
                and_(
                    DiscountAndSKUORM.sku_id == sku_id,
                    DiscountORM.status == DiscountStatus.active.value,
                )
            )
        )
        return [Discount.model_validate(x) for x in rows.all()]

    async def get_max_sku_discount(self, sku_id: UUID) -> float:
        discounts = await self.get_actual_by_sku_id(sku_id)
        if not discounts:
            return 0
        return max([x.percentage for x in discounts])
