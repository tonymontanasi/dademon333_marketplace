import logging

from application.database.models.good import Good, GoodStock
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.sku_repository import SKURepository

logger = logging.getLogger(__name__)


def get_good_cost(
    sku_base_price: float,
    sku_discount: float,
    good: Good,
) -> float:
    if good.stock == GoodStock.valid:
        good_discount = sku_discount
    else:
        good_discount = max(sku_discount, good.discount_percentage)

    return round(sku_base_price * (1 - good_discount / 100), 2)


async def fetch_good_cost(
    good: Good,
    sku_repository: SKURepository,
    discount_repository: DiscountRepository,
) -> float:
    sku = await sku_repository.get_by_id(good.sku_id)
    logger.info(f"Нашли SKU {sku.id}")

    sku_discount = await discount_repository.get_max_sku_discount(sku.id)
    logger.info(f"Скидка на группу товаров {sku.id}: {sku_discount}")

    return get_good_cost(
        sku_base_price=sku.base_price, sku_discount=sku_discount, good=good
    )
