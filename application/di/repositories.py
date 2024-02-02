from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.connection import async_session
from application.database.repositories.acceptance_repository import (
    AcceptanceRepository,
)
from application.database.repositories.discount_and_sku_repository import (
    DiscountAndSKURepository,
)
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.sku_repository import SKURepository
from application.database.repositories.task_repository import TaskRepository


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session.begin() as session:
        yield session


def get_acceptance_repository(db=Depends(get_db)) -> AcceptanceRepository:
    return AcceptanceRepository(db)


def get_good_repository(db=Depends(get_db)) -> GoodRepository:
    return GoodRepository(db)


def get_sku_repository(db=Depends(get_db)) -> SKURepository:
    return SKURepository(db)


def get_task_repository(db=Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_discount_repository(db=Depends(get_db)) -> DiscountRepository:
    return DiscountRepository(db)


def get_discount_and_sku_repository(
    db=Depends(get_db),
) -> DiscountAndSKURepository:
    return DiscountAndSKURepository(db)
