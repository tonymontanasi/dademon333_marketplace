from uuid import UUID

from fastapi import APIRouter, Query, Depends

from application.di.goods import (
    get_get_item_info_use_case,
    get_get_item_info_by_sku_id,
)
from application.use_cases.goods.dto.get_item_info import GetItemInfoOutputDTO
from application.use_cases.goods.dto.get_item_info_by_sku_id import (
    GetItemInfoBySKUIdOutputDTO,
)
from application.use_cases.goods.get_item_info import GetItemInfoUseCase
from application.use_cases.goods.get_item_info_by_sku_id import (
    GetItemInfoBySKUIdUseCase,
)

good_router = APIRouter()


@good_router.get("/getItemInfo")
async def get_item_info(
    item_id: UUID = Query(..., alias="id"),
    use_case: GetItemInfoUseCase = Depends(get_get_item_info_use_case),
) -> GetItemInfoOutputDTO:
    """Получение информации о товаре"""
    return await use_case.execute(item_id)


@good_router.get("/getItemInfoBySKUId")
async def get_item_info_by_sku_id(
    sku_id: UUID = Query(..., alias="id"),
    use_case: GetItemInfoBySKUIdUseCase = Depends(get_get_item_info_by_sku_id),
) -> GetItemInfoBySKUIdOutputDTO:
    """Получение информации о товарах по SKU"""
    return await use_case.execute(sku_id)
