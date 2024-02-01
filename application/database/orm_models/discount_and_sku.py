from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import Mapped

from application.database.orm_models.meta import Base


class DiscountAndSKUORM(Base):
    __tablename__ = "discounts_and_skus"

    discount_id: Mapped[UUID] = Column(
        UUID,
        ForeignKey('discounts.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    sku_id: Mapped[UUID] = Column(
        UUID,
        ForeignKey('sku.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
