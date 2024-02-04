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
