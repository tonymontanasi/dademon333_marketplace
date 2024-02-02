from uuid import UUID

from sqlalchemy import select, func, and_

from application.database.models.good import Good, UpdateGood
from application.database.orm_models import GoodORM
from application.database.repositories.base_repository import BaseDbRepository


class GoodRepository(BaseDbRepository[Good, UpdateGood, GoodORM]):
    _model = Good
    _table = GoodORM

    async def count_available_by_sku_id(self, sku_id: UUID) -> int:
        rows = await self.db_session.scalars(
            select(func.count(GoodORM.id).label("available_count")).where(
                and_(
                    GoodORM.sku_id == sku_id,
                    GoodORM.is_reserved.is_(False),
                    GoodORM.is_sold.is_(False),
                )
            )
        )
        return rows.one()["available_count"]

    async def get_by_sku_id_with_reserved(self, sku_id: UUID) -> list[Good]:
        rows = await self.db_session.scalars(
            select(GoodORM).where(
                and_(
                    GoodORM.sku_id == sku_id,
                    GoodORM.is_sold.is_(False),
                )
            )
        )
        return [Good.model_validate(x) for x in rows.all()]
