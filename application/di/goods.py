from fastapi import Depends

from application.database.repositories.good_repository import GoodRepository
from application.di.repositories import get_good_repository
from application.use_cases.goods.get_item_info import GetItemInfoUseCase


def get_get_item_info_use_case(
    good_repository: GoodRepository = Depends(get_good_repository),
) -> GetItemInfoUseCase:
    return GetItemInfoUseCase(good_repository)
