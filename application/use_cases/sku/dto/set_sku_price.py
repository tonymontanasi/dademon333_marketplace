from uuid import UUID

from pydantic import Field, BaseModel


class SetSKUPriceInputDTO(BaseModel):
    sku_id: UUID
    base_price: float = Field(..., ge=0.0)
