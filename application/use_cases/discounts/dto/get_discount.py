from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.database.models.discount import DiscountStatus


class GetDiscountOutputDTO(BaseModel):
    id: UUID
    status: DiscountStatus
    created_at: datetime
    percentage: float
    sku_ids: list[UUID]
