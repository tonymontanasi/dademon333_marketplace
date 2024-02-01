from enum import StrEnum

from application.database.models.base import ModelBase


class AcceptanceStatus(StrEnum):
    in_work = "in_work"
    completed = "completed"


class Acceptance(ModelBase):
    """Приёмка товара"""
    status: AcceptanceStatus
