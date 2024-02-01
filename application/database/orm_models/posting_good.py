from sqlalchemy import Column, UUID, ForeignKey, VARCHAR, Float

from application.database.orm_models import Base


class PostingGoodORM(Base):
    __tablename__ = "posting_goods"

    posting_id = Column(
        UUID,
        ForeignKey('postings.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    good_id = Column(
        UUID,
        ForeignKey('goods.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    good_stock = Column(VARCHAR, nullable=False)
    cost = Column(Float, nullable=False)
    is_canceled = Column(VARCHAR, nullable=False, server_default="f")
