from uuid import UUID

from fastapi import APIRouter, Query, Depends

from application.di.discounts import get_get_discount_use_case
from application.use_cases.discounts.dto.get_discount import (
    GetDiscountOutputDTO,
)
from application.use_cases.discounts.get_discount import GetDiscountUseCase

discount_router = APIRouter()


@discount_router.get("/getDiscount")
async def get_discount(
    discount_id: UUID = Query(..., alias="id"),
    use_case: GetDiscountUseCase = Depends(get_get_discount_use_case),
) -> GetDiscountOutputDTO:
    """Получение информации об акции"""
    return await use_case.execute(discount_id)
