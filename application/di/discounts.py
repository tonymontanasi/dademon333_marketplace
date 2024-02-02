from fastapi import Depends

from application.di.repositories import (
    get_discount_repository,
    get_discount_and_sku_repository,
)
from application.use_cases.discounts.get_discount import GetDiscountUseCase


def get_get_discount_use_case(
    discount_repository=Depends(get_discount_repository),
    discount_and_sku_repository=Depends(get_discount_and_sku_repository),
) -> GetDiscountUseCase:
    return GetDiscountUseCase(
        discount_repository=discount_repository,
        discount_and_sku_repository=discount_and_sku_repository,
    )
