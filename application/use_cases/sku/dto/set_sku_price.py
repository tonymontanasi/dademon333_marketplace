from uuid import UUID

from pydantic import Field


class SetSKUPriceInputDTO:
    sku_id: UUID
    base_price: float = Field(..., ge=0.0)
