from fastapi import Depends

from application.di.repositories import get_acceptance_repository, \
    get_sku_repository, get_task_repository
from application.use_cases.acceptances.create_acceptance import \
    CreateAcceptanceUseCase


def get_create_acceptance_use_case(
    acceptance_repository=Depends(get_acceptance_repository),
    sku_repository=Depends(get_sku_repository),
    task_repository=Depends(get_task_repository)
) -> CreateAcceptanceUseCase:
    return CreateAcceptanceUseCase(
        acceptance_repository=acceptance_repository,
        sku_repository=sku_repository,
        task_repository=task_repository,
    )
