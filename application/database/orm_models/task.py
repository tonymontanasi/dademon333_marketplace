from sqlalchemy import Column, VARCHAR, UUID, ForeignKey, BigInteger

from application.database.orm_models import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    type = Column(VARCHAR, nullable=False)
    status = Column(VARCHAR, nullable=False, default="in_work", server_default="in_work")
    posting_id = Column(
        UUID,
        ForeignKey("postings.id", onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        index=True
    )
    acceptance_id = Column(
        UUID,
        ForeignKey("acceptances.id", onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        index=True
    )
    good_id = Column(
        UUID,
        ForeignKey("goods.id", onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        index=True
    )
    sku_id = Column(
        UUID,
        ForeignKey("sku.id", onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        index=True
    )
    stock = Column(VARCHAR, nullable=True)
    count = Column(BigInteger, nullable=True)
