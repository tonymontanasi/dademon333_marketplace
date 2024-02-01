from enum import StrEnum
from uuid import UUID

from application.database.models.base import ModelBase, UpdateModelBase


class GoodStock(StrEnum):
    valid = "valid"
    defect = "defect"
    not_found = "not_found"


class GoodStockWithoutNotFound(StrEnum):
    valid = "valid"
    defect = "defect"


class Good(ModelBase):
    """Единица товара на складе"""
    sku_id: UUID
    stock: GoodStock
    discount_percentage: float = 0.0
    is_reserved: bool = False
    is_sold: bool = False


class UpdateGood(UpdateModelBase):
    sku_id: UUID | None = None
    stock: GoodStock | None = None
    discount_percentage: float | None = None
    is_reserved: bool | None = None
    is_sold: bool = None
