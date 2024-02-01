from sqlalchemy import Column, VARCHAR

from application.database.orm_models import Base


class PostingORM(Base):
    __tablename__ = "postings"

    status = Column(VARCHAR, nullable=False)
