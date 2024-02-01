from sqlalchemy import VARCHAR, Column

from application.database.orm_models.meta import Base


class AcceptanceORM(Base):
    __tablename__ = "acceptances"
    status = Column(VARCHAR, nullable=False)
