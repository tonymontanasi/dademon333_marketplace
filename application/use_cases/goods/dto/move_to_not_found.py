from uuid import UUID

from pydantic import BaseModel


class MoveToNotFoundInputDTO(BaseModel):
    id: UUID
