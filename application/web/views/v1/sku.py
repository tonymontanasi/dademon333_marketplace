from fastapi import APIRouter, Response, status, Depends

from application.di.sku import get_toggle_is_hidden_use_case
from application.use_cases.sku.dto.toggle_is_hidden import (
    ToggleIsHiddenInputDTO,
)
from application.use_cases.sku.toggle_is_hidden import ToggleIsHiddenUseCase

sku_router = APIRouter()


@sku_router.post("/toggleIsHidden")
async def toggle_is_hidden(
    input_dto: ToggleIsHiddenInputDTO,
    use_case: ToggleIsHiddenUseCase = Depends(get_toggle_is_hidden_use_case),
):
    """Переключение видимости SKU"""
    await use_case.execute(input_dto)
    return Response(status_code=status.HTTP_200_OK)
