from uuid import UUID

from pydantic import BaseModel


class ToggleIsHiddenInputDTO(BaseModel):
    sku_id: UUID
    is_hidden: bool
