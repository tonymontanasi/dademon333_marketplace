from application.database.models.discount import Discount, UpdateDiscount
from application.database.orm_models import DiscountORM
from application.database.repositories.base_repository import BaseDbRepository


class DiscountRepository(
    BaseDbRepository[Discount, UpdateDiscount, DiscountORM]
):
    _model = Discount
    _table = DiscountORM
