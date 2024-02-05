from fastapi import Depends

from application.di.repositories import get_task_repository
from application.use_cases.tasks.get_task_info import GetTaskInfoUseCase


def get_get_task_info_use_case(
    task_repository=Depends(get_task_repository),
) -> GetTaskInfoUseCase:
    return GetTaskInfoUseCase(task_repository=task_repository)
