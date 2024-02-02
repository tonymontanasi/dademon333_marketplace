from uuid import UUID

from pydantic import BaseModel

from application.database.models.good import GoodStock


class GetItemInfoBySKUIdItemOutputDTO(BaseModel):
    item_id: UUID
    stock: GoodStock
    reserved_state: bool


class GetItemInfoBySKUIdOutputDTO(BaseModel):
    items: list[GetItemInfoBySKUIdItemOutputDTO]
