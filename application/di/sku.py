from fastapi import Depends

from application.di.repositories import get_sku_repository
from application.use_cases.sku.set_sku_price import SetSKUPriceUseCase
from application.use_cases.sku.toggle_is_hidden import ToggleIsHiddenUseCase


def get_toggle_is_hidden_use_case(
    sku_repository=Depends(get_sku_repository),
) -> ToggleIsHiddenUseCase:
    return ToggleIsHiddenUseCase(sku_repository)


def get_set_sku_price_use_case(
    sku_repository=Depends(get_sku_repository),
) -> SetSKUPriceUseCase:
    return SetSKUPriceUseCase(sku_repository)
