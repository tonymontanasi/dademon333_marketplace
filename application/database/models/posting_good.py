from enum import StrEnum
from uuid import UUID

from application.database.models.base import ModelBase, UpdateModelBase
from application.database.models.good import GoodStock


class PostingGoodCancelReason(StrEnum):
    """Причина удаления товара из заказа"""

    not_found = "not_found"  # Товар утерян
    discounted = "discounted"  # Товар уценён


class PostingGood(ModelBase):
    """Товар в заказе клиента"""

    posting_id: UUID
    sku_id: UUID
    good_id: UUID
    good_stock: GoodStock
    cost: float
    cancel_reason: PostingGoodCancelReason | None = None


class UpdatePostingGood(UpdateModelBase):
    posting_id: UUID | None = None
    sku_id: UUID | None = None
    good_id: UUID | None = None
    good_stock: GoodStock | None = None
    cost: float | None = None
    cancel_reason: PostingGoodCancelReason | None = None
