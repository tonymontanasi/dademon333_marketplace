from fastapi import APIRouter, Depends

from application.di.postings import get_create_posting_use_case
from application.use_cases.postings.create_posting import CreatePostingUseCase
from application.use_cases.postings.dto.create_posting import (
    CreatePostingInputDTO,
    CreatePostingOutputDTO,
)

posting_router = APIRouter()


@posting_router.post("/createPosting")
async def create_posting(
    input_dto: CreatePostingInputDTO,
    use_case: CreatePostingUseCase = Depends(get_create_posting_use_case),
) -> CreatePostingOutputDTO:
    """Создание заказа"""
    return await use_case.execute(input_dto)
