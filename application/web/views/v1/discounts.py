from uuid import UUID

from fastapi import APIRouter, Query, Depends, Response, status

from application.di.discounts import (
    get_get_discount_use_case,
    get_create_discount_use_case,
    get_cancel_discount_use_case,
)
from application.use_cases.discounts.cancel_discount import (
    CancelDiscountUseCase,
)
from application.use_cases.discounts.create_discount import (
    CreateDiscountUseCase,
)
from application.use_cases.discounts.dto.cancel_discount import (
    CancelDiscountInputDTO,
)
from application.use_cases.discounts.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)
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


@discount_router.post("/createDiscount")
async def create_discount(
    input_dto: CreateDiscountInputDTO,
    use_case: CreateDiscountUseCase = Depends(get_create_discount_use_case),
) -> CreateDiscountOutputDTO:
    """Создание скидки"""
    return await use_case.execute(input_dto)


@discount_router.post("/cancelDiscount")
async def cancel_discount(
    input_dto: CancelDiscountInputDTO,
    use_case: CancelDiscountUseCase = Depends(get_cancel_discount_use_case),
):
    """Закрытие скидки"""
    await use_case.execute(input_dto)
    return Response(status_code=status.HTTP_200_OK)
