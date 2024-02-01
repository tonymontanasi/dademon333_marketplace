from fastapi import APIRouter, Depends

from application.di.acceptance import get_create_acceptance_use_case
from application.use_cases.acceptances.create_acceptance import \
    CreateAcceptanceUseCase
from application.use_cases.acceptances.dto.create_acceptance import \
    CreateAcceptanceInputDTO, CreateAcceptanceOutputDTO

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
