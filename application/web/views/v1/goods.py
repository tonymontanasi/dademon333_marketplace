from uuid import UUID

from fastapi import APIRouter, Query, Depends

from application.di.goods import get_get_item_info_use_case
from application.use_cases.goods.dto.get_item_info import GetItemInfoOutputDTO
from application.use_cases.goods.get_item_info import GetItemInfoUseCase

good_router = APIRouter()


@good_router.get("/getItemInfo")
async def get_item_info(
    item_id: UUID = Query(..., alias="id"),
    use_case: GetItemInfoUseCase = Depends(get_get_item_info_use_case),
) -> GetItemInfoOutputDTO:
    """Получение информации о товаре"""
    return await use_case.execute(item_id)
