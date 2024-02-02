from fastapi import Depends

from application.di.repositories import get_good_repository
from application.use_cases.goods.get_item_info import GetItemInfoUseCase
from application.use_cases.goods.get_item_info_by_sku_id import (
    GetItemInfoBySKUIdUseCase,
)


def get_get_item_info_use_case(
    good_repository=Depends(get_good_repository),
) -> GetItemInfoUseCase:
    return GetItemInfoUseCase(good_repository)


def get_get_item_info_by_sku_id(
    good_repository=Depends(get_good_repository),
) -> GetItemInfoBySKUIdUseCase:
    return GetItemInfoBySKUIdUseCase(good_repository)
