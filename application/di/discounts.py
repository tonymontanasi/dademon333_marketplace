from fastapi import Depends

from application.di.repositories import (
    get_discount_repository,
    get_discount_and_sku_repository,
    get_sku_repository,
)
from application.use_cases.discounts.cancel_discount import (
    CancelDiscountUseCase,
)
from application.use_cases.discounts.create_discount import (
    CreateDiscountUseCase,
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


def get_create_discount_use_case(
    sku_repository=Depends(get_sku_repository),
    discount_repository=Depends(get_discount_repository),
    discount_and_sku_repository=Depends(get_discount_and_sku_repository),
) -> CreateDiscountUseCase:
    return CreateDiscountUseCase(
        sku_repository=sku_repository,
        discount_repository=discount_repository,
        discount_and_sku_repository=discount_and_sku_repository,
    )


def get_cancel_discount_use_case(
    discount_repository=Depends(get_discount_repository),
) -> CancelDiscountUseCase:
    return CancelDiscountUseCase(discount_repository=discount_repository)
