from sqlalchemy import UUID, Column, ForeignKey, VARCHAR, Float, Index

from application.database.orm_models.meta import Base


class GoodORM(Base):
    __tablename__ = "goods"

    sku_id = Column(
        UUID,
        ForeignKey('sku.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    stock = Column(VARCHAR, nullable=False)
    discount_percentage = Column(Float, nullable=False, server_default="0.0")
    is_reserved = Column(VARCHAR, nullable=False, server_default="f")
    is_sold = Column(VARCHAR, nullable=False, server_default="f")

    __table_args__ = (
        Index("ix_goods_sku_id_is_sold", "sku_id", "is_sold"),
    )
