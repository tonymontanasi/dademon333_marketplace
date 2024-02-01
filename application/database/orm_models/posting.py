from sqlalchemy import Column, VARCHAR

from application.database.orm_models import Base


class PostingORM(Base):
    __tablename__ = "postings"

    status = Column(VARCHAR, nullable=False, default="in_item_pick", server_default="in_item_pick")
