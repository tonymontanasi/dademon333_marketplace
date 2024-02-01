from uuid import UUID

from application.database.models.base import ModelBase


class DiscountAndSKU(ModelBase):
    """Связь многие-ко-многим между скидкой (распродажей) и группой товаров."""
    discount_id: UUID
    sku_id: UUID


class UpdateDiscountAndSKU(ModelBase):
    discount_id: UUID | None = None
    sku_id: UUID | None = None
