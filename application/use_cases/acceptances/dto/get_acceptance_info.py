from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.database.models.good import GoodStock
from application.database.models.task import TaskStatus


class GetAcceptanceInfoAcceptedItemOutputDTO(BaseModel):
    sku_id: UUID
    stock: GoodStock
    count: int


class GetAcceptanceInfoTaskOutputDTO(BaseModel):
    id: UUID
    status: TaskStatus


class GetAcceptanceInfoOutputDTO(BaseModel):
    id: UUID
    created_at: datetime
    accepted: list[GetAcceptanceInfoAcceptedItemOutputDTO]
    task_ids: list[GetAcceptanceInfoTaskOutputDTO]
