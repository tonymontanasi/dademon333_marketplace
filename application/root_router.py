from fastapi import APIRouter
from application.web.views.v1.acceptances import acceptance_router
from application.web.views.v1.discounts import discount_router

root_router = APIRouter()

root_router.include_router(
    acceptance_router,
    tags=["Acceptances"],
)
root_router.include_router(
    discount_router,
    tags=["Discounts"],
)
