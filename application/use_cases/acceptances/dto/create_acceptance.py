from collections import defaultdict
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ValidationError

from application.database.models.good import GoodStockWithoutNotFound


class CreateAcceptanceItemInputDTO(BaseModel):
    sku_id: UUID
    stock: GoodStockWithoutNotFound
    count: int = Field(..., ge=1, le=999)


class CreateAcceptanceInputDTO(BaseModel):
    items_to_accept: list[CreateAcceptanceItemInputDTO] = Field(
        ..., min_length=1
    )

    @field_validator("items_to_accept")
    @classmethod
    def validate_items_count(cls, v: list[CreateAcceptanceItemInputDTO]):
        count_by_sku = defaultdict(int)
        for item in v:
            count_by_sku[item.sku_id] += item.count
            if count_by_sku[item.sku_id] > 999:
                raise ValidationError()


class CreateAcceptanceOutputDTO(BaseModel):
    id: UUID
