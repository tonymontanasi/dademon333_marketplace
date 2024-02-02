from fastapi import Depends

from application.di.repositories import (
    get_sku_repository,
    get_good_repository,
    get_discount_repository,
)
from application.use_cases.sku.get_sku_info import GetSKUInfoUseCase
from application.use_cases.sku.set_sku_price import SetSKUPriceUseCase
from application.use_cases.sku.toggle_is_hidden import ToggleIsHiddenUseCase


def get_get_sku_info_use_case(
    sku_repository=Depends(get_sku_repository),
    good_repository=Depends(get_good_repository),
    discount_repository=Depends(get_discount_repository),
) -> GetSKUInfoUseCase:
    return GetSKUInfoUseCase(
        sku_repository=sku_repository,
        good_repository=good_repository,
        discount_repository=discount_repository,
    )


def get_toggle_is_hidden_use_case(
    sku_repository=Depends(get_sku_repository),
) -> ToggleIsHiddenUseCase:
    return ToggleIsHiddenUseCase(sku_repository)


def get_set_sku_price_use_case(
    sku_repository=Depends(get_sku_repository),
) -> SetSKUPriceUseCase:
    return SetSKUPriceUseCase(sku_repository)
