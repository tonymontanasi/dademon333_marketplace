from uuid import UUID

from sqlalchemy import select, update, and_

from application.database.models.posting_good import (
    PostingGood,
    UpdatePostingGood,
    PostingGoodCancelReason,
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

    async def remove_from_posting(
        self,
        good_id: UUID,
        posting_id: UUID,
        cancel_reason: PostingGoodCancelReason,
    ) -> None:
        await self.db_session.execute(
            update(PostingGoodORM)
            .where(
                and_(
                    PostingGoodORM.good_id == good_id,
                    PostingGoodORM.posting_id == posting_id,
                )
            )
            .values(cancel_reason=cancel_reason.value)
        )
