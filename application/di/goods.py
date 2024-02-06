from fastapi import Depends

from application.di.repositories import (
    get_good_repository,
    get_sku_repository,
    get_task_repository,
    get_discount_repository,
    get_posting_good_repository,
)
from application.use_cases.goods.get_item_info import GetItemInfoUseCase
from application.use_cases.goods.get_item_info_by_sku_id import (
    GetItemInfoBySKUIdUseCase,
)
from application.use_cases.goods.markdown_item import MarkdownItemUseCase
from application.use_cases.goods.move_to_not_found import MoveToNotFoundUseCase
from application.use_cases.goods.try_pick_new_good import TryPickNewGoodUseCase


def get_get_item_info_use_case(
    good_repository=Depends(get_good_repository),
) -> GetItemInfoUseCase:
    return GetItemInfoUseCase(good_repository)


def get_get_item_info_by_sku_id(
    good_repository=Depends(get_good_repository),
) -> GetItemInfoBySKUIdUseCase:
    return GetItemInfoBySKUIdUseCase(good_repository)


def get_try_pick_new_good_use_case(
    sku_repository=Depends(get_sku_repository),
    good_repository=Depends(get_good_repository),
    task_repository=Depends(get_task_repository),
    discount_repository=Depends(get_discount_repository),
    posting_good_repository=Depends(get_posting_good_repository),
) -> TryPickNewGoodUseCase:
    return TryPickNewGoodUseCase(
        sku_repository=sku_repository,
        good_repository=good_repository,
        task_repository=task_repository,
        discount_repository=discount_repository,
        posting_good_repository=posting_good_repository,
    )


def get_move_to_not_found_use_case(
    good_repository=Depends(get_good_repository),
    task_repository=Depends(get_task_repository),
    posting_good_repository=Depends(get_posting_good_repository),
    picking_use_case=Depends(get_try_pick_new_good_use_case),
) -> MoveToNotFoundUseCase:
    return MoveToNotFoundUseCase(
        good_repository=good_repository,
        task_repository=task_repository,
        posting_good_repository=posting_good_repository,
        picking_use_case=picking_use_case,
    )


def get_markdown_item_use_case(
    good_repository=Depends(get_good_repository),
    task_repository=Depends(get_task_repository),
    posting_good_repository=Depends(get_posting_good_repository),
    picking_use_case=Depends(get_try_pick_new_good_use_case),
) -> MarkdownItemUseCase:
    return MarkdownItemUseCase(
        good_repository=good_repository,
        task_repository=task_repository,
        posting_good_repository=posting_good_repository,
        picking_use_case=picking_use_case,
    )
