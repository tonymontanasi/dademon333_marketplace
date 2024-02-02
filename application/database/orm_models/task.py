import uuid

from sqlalchemy import Column, VARCHAR, UUID, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped

from application.database.orm_models import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    type: Mapped[str] = Column(VARCHAR, nullable=False)
    status: Mapped[str] = Column(
        VARCHAR, nullable=False, default="in_work", server_default="in_work"
    )
    posting_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("postings.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    acceptance_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("acceptances.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    good_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("goods.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    sku_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("sku.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    stock: Mapped[str] = Column(VARCHAR, nullable=False)
    count: Mapped[int] = Column(BigInteger, nullable=False)
