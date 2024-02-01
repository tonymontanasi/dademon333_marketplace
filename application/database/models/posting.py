from enum import StrEnum

from application.database.models.base import ModelBase, UpdateModelBase


class PostingStatus(StrEnum):
    in_item_pick = "in_item_pick"
    sent = "sent"
    canceled = "canceled"


class Posting(ModelBase):
    """Заказ клиента"""
    status: PostingStatus


class UpdatePosting(UpdateModelBase):
    status: PostingStatus | None = None
