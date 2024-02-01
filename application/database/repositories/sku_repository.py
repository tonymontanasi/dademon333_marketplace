from application.database.models.sku import SKU, UpdateSKU
from application.database.orm_models import SKUORM
from application.database.repositories.base_repository import BaseDbRepository


class SKURepository(BaseDbRepository[SKU, UpdateSKU, SKUORM]):
    _model = SKU
    _table = SKUORM
