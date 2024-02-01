from sqlalchemy import VARCHAR, Column
from sqlalchemy.orm import Mapped

from application.database.orm_models.meta import Base


class AcceptanceORM(Base):
    __tablename__ = "acceptances"
    status: Mapped[str] = Column(VARCHAR, nullable=False, default="in_work", server_default="in_work")
