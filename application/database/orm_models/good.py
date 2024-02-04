import uuid

from sqlalchemy import UUID, Column, ForeignKey, VARCHAR, Float, Index, Boolean
from sqlalchemy.orm import Mapped

from application.database.orm_models.meta import Base


class GoodORM(Base):
    __tablename__ = "goods"

    sku_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("sku.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    stock: Mapped[str] = Column(VARCHAR, nullable=False)
    discount_percentage: Mapped[float] = Column(
        Float, nullable=False, server_default="0.0"
    )
    is_reserved: Mapped[bool] = Column(
        Boolean, nullable=False, default=False, server_default="f"
    )
    is_sold: Mapped[bool] = Column(
        Boolean, nullable=False, default=False, server_default="f"
    )

    __table_args__ = (Index("ix_goods_sku_id_is_sold", "sku_id", "is_sold"),)
