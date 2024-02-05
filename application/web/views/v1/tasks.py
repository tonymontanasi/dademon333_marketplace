from uuid import UUID

from fastapi import APIRouter, Query, Depends

from application.di.tasks import get_get_task_info_use_case
from application.use_cases.tasks.dto.get_task_info import GetTaskInfoOutputDTO
from application.use_cases.tasks.get_task_info import GetTaskInfoUseCase

task_router = APIRouter()


@task_router.get("/getTaskInfo")
async def get_task_info(
    task_id: UUID = Query(..., alias="id"),
    use_case: GetTaskInfoUseCase = Depends(get_get_task_info_use_case),
) -> GetTaskInfoOutputDTO:
    """Получение информации о задаче"""
    return await use_case.execute(task_id)
