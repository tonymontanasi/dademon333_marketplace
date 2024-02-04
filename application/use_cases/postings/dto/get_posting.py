from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.database.models.posting import PostingStatus
from application.database.models.task import TaskStatus


class GetPostingGoodOutputDTO(BaseModel):
    sku: UUID
    from_valid_ids: list[UUID]
    from_defect_ids: list[UUID]


class GetPostingTaskOutputDTO(BaseModel):
    id: UUID
    status: TaskStatus


class GetPostingOutputDTO(BaseModel):
    id: UUID
    status: PostingStatus
    created_at: datetime
    cost: float
    ordered_goods: list[GetPostingGoodOutputDTO]
    not_found: list[UUID]
    task_ids: list[GetPostingTaskOutputDTO]
