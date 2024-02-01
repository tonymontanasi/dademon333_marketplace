from uuid import UUID

from application.database.models.base import ModelBase, UpdateModelBase
from application.database.models.good import GoodStock


class PostingGood(ModelBase):
    """Товар в заказе клиента"""
    posting_id: UUID
    sku_id: UUID
    good_id: UUID
    good_stock: GoodStock
    cost: float
    is_canceled: bool = False  # Если товар утерян или уценён во время сборки


class UpdatePostingGood(UpdateModelBase):
    posting_id: UUID | None = None
    sku_id: UUID | None = None
    good_id: UUID | None = None
    good_stock: GoodStock | None = None
    cost: float | None = None
    is_canceled: bool | None = None
