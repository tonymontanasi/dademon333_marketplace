from uuid import UUID

from sqlalchemy import select

from application.database.models.posting_good import (
    PostingGood,
    UpdatePostingGood,
)
from application.database.orm_models import PostingGoodORM
from application.database.repositories.base_repository import BaseDbRepository


class PostingGoodRepository(
    BaseDbRepository[PostingGood, UpdatePostingGood, PostingGoodORM]
):
    _model = PostingGood
    _table = PostingGoodORM

    async def get_by_posting_id(self, posting_id: UUID) -> list[PostingGood]:
        rows = await self.db_session.scalars(
            select(PostingGoodORM).where(
                PostingGoodORM.posting_id == posting_id
            )
        )
        return [PostingGood.model_validate(x) for x in rows.all()]
