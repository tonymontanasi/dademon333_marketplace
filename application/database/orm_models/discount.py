from sqlalchemy import Column, Float, VARCHAR
from sqlalchemy.orm import Mapped

from application.database.orm_models.meta import Base


class DiscountORM(Base):
    __tablename__ = "discounts"

    percentage: Mapped[float] = Column(Float, nullable=False)
    status: Mapped[str] = Column(VARCHAR, nullable=False, default="active", server_default="active")
