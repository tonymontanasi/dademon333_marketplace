from uuid import UUID

from fastapi import APIRouter, Depends, Query

from application.di.acceptance import (
    get_create_acceptance_use_case,
    get_get_acceptance_info_use_case,
)
from application.use_cases.acceptances.create_acceptance import (
    CreateAcceptanceUseCase,
)
from application.use_cases.acceptances.dto.create_acceptance import (
    CreateAcceptanceInputDTO,
    CreateAcceptanceOutputDTO,
)
from application.use_cases.acceptances.dto.get_acceptance_info import (
    GetAcceptanceInfoOutputDTO,
)
from application.use_cases.acceptances.get_acceptance_info import (
    GetAcceptanceInfoUseCase,
)

acceptance_router = APIRouter()


@acceptance_router.post("/createAcceptance")
async def create_acceptance(
    input_dto: CreateAcceptanceInputDTO,
    use_case: CreateAcceptanceUseCase = Depends(
        get_create_acceptance_use_case
    ),
) -> CreateAcceptanceOutputDTO:
    """Создание приёмки"""
    return await use_case.execute(input_dto)


@acceptance_router.get("/getAcceptanceInfo")
async def get_acceptance_info(
    id_: UUID = Query(..., alias="id"),
    use_case: GetAcceptanceInfoUseCase = Depends(
        get_get_acceptance_info_use_case
    ),
) -> GetAcceptanceInfoOutputDTO:
    """Получение информации о приёмке"""
    return await use_case.execute(acceptance_id=id_)
