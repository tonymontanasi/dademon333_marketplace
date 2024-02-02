from uuid import UUID

from pydantic import BaseModel, Field


class CreateDiscountInputDTO(BaseModel):
    sku_ids: list[UUID] = Field(..., min_length=1)
    percentage: float


class CreateDiscountOutputDTO(BaseModel):
    id: UUID
