from fastapi import Depends

from application.di.goods import get_try_pick_new_good_use_case
from application.di.repositories import (
    get_task_repository,
    get_good_repository,
    get_posting_repository,
    get_posting_good_repository,
    get_acceptance_repository,
)
from application.use_cases.tasks.finish_task import FinishTaskUseCase
from application.use_cases.tasks.get_task_info import GetTaskInfoUseCase


def get_get_task_info_use_case(
    task_repository=Depends(get_task_repository),
) -> GetTaskInfoUseCase:
    return GetTaskInfoUseCase(task_repository=task_repository)


def get_finish_task_use_case(
    task_repository=Depends(get_task_repository),
    good_repository=Depends(get_good_repository),
    posting_repository=Depends(get_posting_repository),
    posting_good_repository=Depends(get_posting_good_repository),
    acceptance_repository=Depends(get_acceptance_repository),
    picking_use_case=Depends(get_try_pick_new_good_use_case),
) -> FinishTaskUseCase:
    return FinishTaskUseCase(
        task_repository=task_repository,
        good_repository=good_repository,
        posting_repository=posting_repository,
        posting_good_repository=posting_good_repository,
        acceptance_repository=acceptance_repository,
        picking_use_case=picking_use_case,
    )
