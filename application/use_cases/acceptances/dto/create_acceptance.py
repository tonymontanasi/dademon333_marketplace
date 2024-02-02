from uuid import UUID

from pydantic import BaseModel, Field

from application.database.models.good import GoodStockWithoutNotFound


class CreateAcceptanceItemInputDTO(BaseModel):
    sku_id: UUID
    stock: GoodStockWithoutNotFound
    count: int = Field(..., ge=1, le=999)


class CreateAcceptanceInputDTO(BaseModel):
    items_to_accept: list[CreateAcceptanceItemInputDTO] = Field(
        ..., min_length=1
    )


class CreateAcceptanceOutputDTO(BaseModel):
    id: UUID
