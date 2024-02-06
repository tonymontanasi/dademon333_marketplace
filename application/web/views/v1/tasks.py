from uuid import UUID

from fastapi import APIRouter, Query, Depends, Response, status

from application.di.tasks import (
    get_get_task_info_use_case,
    get_finish_task_use_case,
)
from application.use_cases.tasks.dto.finish_task import FinishTaskInputDTO
from application.use_cases.tasks.dto.get_task_info import GetTaskInfoOutputDTO
from application.use_cases.tasks.finish_task import FinishTaskUseCase
from application.use_cases.tasks.get_task_info import GetTaskInfoUseCase

task_router = APIRouter()


@task_router.get("/getTaskInfo")
async def get_task_info(
    task_id: UUID = Query(..., alias="id"),
    use_case: GetTaskInfoUseCase = Depends(get_get_task_info_use_case),
) -> GetTaskInfoOutputDTO:
    """Получение информации о задаче"""
    return await use_case.execute(task_id)


@task_router.post("/finishTask")
async def finish_task(
    input_dto: FinishTaskInputDTO,
    use_case: FinishTaskUseCase = Depends(get_finish_task_use_case),
):
    """Завершение задачи"""
    await use_case.execute(input_dto)
    return Response(status_code=status.HTTP_200_OK)
