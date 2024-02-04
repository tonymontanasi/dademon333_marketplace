import uuid

from sqlalchemy import Column, UUID, ForeignKey, VARCHAR, Float, Boolean
from sqlalchemy.orm import Mapped

from application.database.orm_models import Base


class PostingGoodORM(Base):
    __tablename__ = "posting_goods"

    posting_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("postings.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sku_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("sku.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    good_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("goods.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    good_stock: Mapped[str] = Column(VARCHAR, nullable=False)
    cost: Mapped[float] = Column(Float, nullable=False)
    is_canceled: Mapped[bool] = Column(
        Boolean, nullable=False, default=False, server_default="f"
    )
