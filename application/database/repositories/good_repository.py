from application.database.models.good import Good, UpdateGood
from application.database.orm_models import GoodORM
from application.database.repositories.base_repository import BaseDbRepository


class GoodRepository(BaseDbRepository[Good, UpdateGood, GoodORM]):
    _model = Good
    _table = GoodORM
