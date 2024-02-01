from sqlalchemy import Column, UUID, ForeignKey

from application.database.orm_models.meta import Base


class DiscountAndSKUORM(Base):
    __tablename__ = "discounts_and_skus"

    discount_id = Column(
        UUID,
        ForeignKey('discounts.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    sku_id = Column(
        UUID,
        ForeignKey('sku.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
