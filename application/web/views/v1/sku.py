from uuid import UUID

from fastapi import APIRouter, Response, status, Depends, Query

from application.di.sku import (
    get_toggle_is_hidden_use_case,
    get_set_sku_price_use_case,
    get_get_sku_info_use_case,
)
from application.use_cases.sku.dto.get_sku_info import GetSKUInfoOutputDTO
from application.use_cases.sku.dto.set_sku_price import SetSKUPriceInputDTO
from application.use_cases.sku.dto.toggle_is_hidden import (
    ToggleIsHiddenInputDTO,
)
from application.use_cases.sku.get_sku_info import GetSKUInfoUseCase
from application.use_cases.sku.set_sku_price import SetSKUPriceUseCase
from application.use_cases.sku.toggle_is_hidden import ToggleIsHiddenUseCase

sku_router = APIRouter()


@sku_router.get("/getSkuInfo")
async def get_sku_info(
    sku_id: UUID = Query(..., alias="id"),
    use_case: GetSKUInfoUseCase = Depends(get_get_sku_info_use_case),
) -> GetSKUInfoOutputDTO:
    """Получение информации о SKU"""
    return await use_case.execute(sku_id)


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
