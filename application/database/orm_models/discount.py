from sqlalchemy import Column, Float, VARCHAR

from application.database.orm_models.meta import Base


class DiscountORM(Base):
    __tablename__ = "discounts"

    percentage = Column(Float, nullable=False)
    status = Column(VARCHAR, nullable=False)
