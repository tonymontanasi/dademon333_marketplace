from sqlalchemy import Column, Float, VARCHAR

from application.database.orm_models import Base


class SKUORM(Base):
    __tablename__ = "sku"

    base_price = Column(Float, nullable=False, server_default="0.0")
    is_hidden = Column(VARCHAR, nullable=False, server_default="t")
