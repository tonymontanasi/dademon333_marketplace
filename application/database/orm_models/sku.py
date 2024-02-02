from sqlalchemy import Column, Float, VARCHAR
from sqlalchemy.orm import Mapped

from application.database.orm_models import Base


class SKUORM(Base):
    __tablename__ = "sku"

    base_price: Mapped[float] = Column(
        Float, nullable=False, server_default="0.0"
    )
    is_hidden: Mapped[str] = Column(
        VARCHAR, nullable=False, server_default="t"
    )
