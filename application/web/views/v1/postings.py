from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from application.di.postings import (
    get_create_posting_use_case,
    get_get_posting_use_case,
    get_cancel_posting_use_case,
)
from application.use_cases.postings.cancel_posting import CancelPostingUseCase
from application.use_cases.postings.create_posting import CreatePostingUseCase
from application.use_cases.postings.dto.cancel_posting import (
    CancelPostingInputDTO,
)
from application.use_cases.postings.dto.create_posting import (
    CreatePostingInputDTO,
    CreatePostingOutputDTO,
)
from application.use_cases.postings.dto.get_posting import GetPostingOutputDTO
from application.use_cases.postings.get_posting import GetPostingUseCase

posting_router = APIRouter()


@posting_router.get("/getPosting")
async def get_posting(
    posting_id: UUID = Query(..., alias="id"),
    use_case: GetPostingUseCase = Depends(get_get_posting_use_case),
) -> GetPostingOutputDTO:
    """Получение информации о заказе"""
    return await use_case.execute(posting_id)


@posting_router.post("/createPosting")
async def create_posting(
    input_dto: CreatePostingInputDTO,
    use_case: CreatePostingUseCase = Depends(get_create_posting_use_case),
) -> CreatePostingOutputDTO:
    """Создание заказа"""
    return await use_case.execute(input_dto)


@posting_router.post("/cancelPosting")
async def cancel_posting(
    input_dto: CancelPostingInputDTO,
    use_case: CancelPostingUseCase = Depends(get_cancel_posting_use_case),
):
    """Отмена заказа"""
    await use_case.execute(input_dto)
    return Response(status_code=status.HTTP_200_OK)
