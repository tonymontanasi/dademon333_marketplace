from uuid import UUID

from sqlalchemy import select, func, and_, update

from application.database.models.good import Good, UpdateGood, GoodStock
from application.database.orm_models import GoodORM
from application.database.repositories.base_repository import BaseDbRepository


class GoodRepository(BaseDbRepository[Good, UpdateGood, GoodORM]):
    _model = Good
    _table = GoodORM

    async def count_by_sku_id(self, sku_id: UUID) -> int:
        rows = await self.db_session.scalars(
            select(func.count(GoodORM.id).label("available_count")).where(
                and_(
                    GoodORM.sku_id == sku_id,
                    GoodORM.is_sold.is_(False),
                )
            )
        )
        return rows.one()["available_count"]

    async def get_by_sku_id(self, sku_id: UUID) -> list[Good]:
        rows = await self.db_session.scalars(
            select(GoodORM).where(
                and_(
                    GoodORM.sku_id == sku_id,
                    GoodORM.is_sold.is_(False),
                )
            )
        )
        return [Good.model_validate(x) for x in rows.all()]

    async def pick_available_by_sku(
        self, sku_id: UUID, stock: GoodStock
    ) -> Good | None:
        row = await self.db_session.scalars(
            select(GoodORM)
            .where(
                and_(
                    GoodORM.sku_id == sku_id,
                    GoodORM.stock == stock,
                    GoodORM.is_reserved.is_(False),
                    GoodORM.is_sold.is_(False),
                )
            )
            .limit(1)
        )
        result = row.one_or_none()
        if not result:
            return None
        return Good.model_validate(result)

    async def sell_goods(self, good_ids: list[UUID]) -> None:
        await self.db_session.execute(
            update(GoodORM)
            .where(GoodORM.id.in_(good_ids))
            .values(is_sold=True, is_reserved=False)
        )
