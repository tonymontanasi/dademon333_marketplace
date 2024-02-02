from datetime import datetime
from uuid import UUID, uuid4

from pydantic import ConfigDict, Field, BaseModel


class ModelBase(BaseModel):
    """База для всех моделей."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UpdateModelBase(BaseModel):
    """База для всех update-моделей."""

    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(use_enum_values=True)
