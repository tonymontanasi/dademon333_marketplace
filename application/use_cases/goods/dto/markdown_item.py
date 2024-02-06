from uuid import UUID

from pydantic import BaseModel


class MarkdownItemInputDTO(BaseModel):
    id: UUID
    percentage: float
