from fastapi import APIRouter, Response, status, Depends

from application.di.sku import (
    get_toggle_is_hidden_use_case,
    get_set_sku_price_use_case,
)
from application.use_cases.sku.dto.set_sku_price import SetSKUPriceInputDTO
from application.use_cases.sku.dto.toggle_is_hidden import (
    ToggleIsHiddenInputDTO,
)
from application.use_cases.sku.set_sku_price import SetSKUPriceUseCase
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


@sku_router.post("/setSkuPrice")
async def set_sku_price(
    input_dto: SetSKUPriceInputDTO,
    use_case: SetSKUPriceUseCase = Depends(get_set_sku_price_use_case),
):
    """Переключение стоимости SKU"""
    await use_case.execute(input_dto)
    return Response(status_code=status.HTTP_200_OK)
