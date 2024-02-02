from uuid import UUID

from pydantic import BaseModel


class CancelDiscountInputDTO(BaseModel):
    id: UUID
