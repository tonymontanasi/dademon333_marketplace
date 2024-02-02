import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=func.now(),
    )
