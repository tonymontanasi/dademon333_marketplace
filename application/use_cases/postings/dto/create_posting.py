from uuid import UUID

from pydantic import BaseModel, Field


class CreatePostingGoodInputDTO(BaseModel):
    sku: UUID
    from_valid_ids: list[UUID]
    from_defect_ids: list[UUID]


class CreatePostingInputDTO(BaseModel):
    ordered_goods: list[CreatePostingGoodInputDTO] = Field(..., min_length=1)


class CreatePostingOutputDTO(BaseModel):
    id: UUID
