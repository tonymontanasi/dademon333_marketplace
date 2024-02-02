from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GetSKUInfoOutputDTO(BaseModel):
    id: UUID
    created_at: datetime
    actual_price: float
    base_price: float
    count: int
    is_hidden: bool
