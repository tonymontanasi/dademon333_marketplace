from uuid import UUID

from pydantic import BaseModel


class CancelPostingInputDTO(BaseModel):
    id: UUID
