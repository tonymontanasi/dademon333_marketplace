from enum import StrEnum

from application.database.models.base import ModelBase, UpdateModelBase


class DiscountStatus(StrEnum):
    active = "active"
    finished = "finished"


class Discount(ModelBase):
    """Скидка (распродажа).
    Связь скидки и группы товаров описана в модели DiscountAndSKU.
    """
    percentage: float
    status: DiscountStatus


class UpdateDiscount(UpdateModelBase):
    percentage: float | None = None
    status: DiscountStatus | None = None
