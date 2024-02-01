from application.database.models.base import ModelBase, UpdateModelBase


class SKU(ModelBase):
    base_price: float = 0.0
    is_hidden: bool = True


class UpdateSKU(UpdateModelBase):
    base_price: float | None = None
    is_hidden: bool | None = None
