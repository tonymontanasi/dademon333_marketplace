from application.database.models.posting import Posting, UpdatePosting
from application.database.orm_models import PostingORM
from application.database.repositories.base_repository import BaseDbRepository


class PostingRepository(BaseDbRepository[Posting, UpdatePosting, PostingORM]):
    _model = Posting
    _table = PostingORM
