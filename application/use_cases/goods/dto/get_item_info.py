from uuid import UUID

from pydantic import BaseModel

from application.database.models.good import GoodStock


class GetItemInfoOutputDTO(BaseModel):
    id: UUID
    sku_id: UUID
    stock: GoodStock
    reserved_state: bool
