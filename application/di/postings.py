from fastapi import Depends

from application.di.repositories import (
    get_sku_repository,
    get_good_repository,
    get_task_repository,
    get_discount_repository,
    get_posting_repository,
    get_posting_good_repository,
)
from application.use_cases.postings.create_posting import CreatePostingUseCase


def get_create_posting_use_case(
    sku_repository=Depends(get_sku_repository),
    good_repository=Depends(get_good_repository),
    task_repository=Depends(get_task_repository),
    discount_repository=Depends(get_discount_repository),
    posting_repository=Depends(get_posting_repository),
    posting_good_repository=Depends(get_posting_good_repository),
) -> CreatePostingUseCase:
    return CreatePostingUseCase(
        sku_repository=sku_repository,
        good_repository=good_repository,
        task_repository=task_repository,
        discount_repository=discount_repository,
        posting_repository=posting_repository,
        posting_good_repository=posting_good_repository,
    )
