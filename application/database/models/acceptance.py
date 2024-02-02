from enum import StrEnum

from application.database.models.base import ModelBase, UpdateModelBase


class AcceptanceStatus(StrEnum):
    in_work = "in_work"
    completed = "completed"


class Acceptance(ModelBase):
    """Приёмка товара"""

    status: AcceptanceStatus = AcceptanceStatus.in_work


class UpdateAcceptance(UpdateModelBase):
    status: AcceptanceStatus | None = None
