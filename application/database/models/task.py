from enum import StrEnum
from uuid import UUID

from application.database.models.base import ModelBase, UpdateModelBase
from application.database.models.good import GoodStock


class TaskType(StrEnum):
    acceptance = "acceptance"  # Приёмка товара
    picking = "picking"  # Сборку товара
    placing = "placing"  # Размещение товара на складе


class TaskStatus(StrEnum):
    completed = "completed"
    in_work = "in_work"
    canceled = "canceled"


class Task(ModelBase):
    """Задача на действие с товаром"""
    type: TaskType
    status: TaskStatus = TaskStatus.in_work
    posting_id: UUID | None
    acceptance_id: UUID | None
    good_id: UUID | None
    sku_id: UUID | None
    stock: GoodStock | None
    count: int | None


class UpdateTask(UpdateModelBase):
    type: TaskType | None = None
    status: TaskStatus | None = None
    posting_id: UUID | None = None
    acceptance_id: UUID | None = None
    good_id: UUID | None = None
    sku_id: UUID | None = None
    stock: GoodStock | None = None
    count: int | None = None
