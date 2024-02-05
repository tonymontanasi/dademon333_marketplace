from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.database.models.good import GoodStock
from application.database.models.task import TaskStatus, TaskType


class GetTaskInfoTargetOutputDTO(BaseModel):
    stock: GoodStock
    id: UUID


class GetTaskInfoOutputDTO(BaseModel):
    id: UUID
    status: TaskStatus
    created_at: datetime
    type: TaskType
    task_target: GetTaskInfoTargetOutputDTO
    posting_id: UUID | None
