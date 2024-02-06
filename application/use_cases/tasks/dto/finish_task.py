from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class FinishTaskTaskStatus(StrEnum):
    completed = "completed"
    canceled = "canceled"


class FinishTaskInputDTO(BaseModel):
    id: UUID
    status: FinishTaskTaskStatus
