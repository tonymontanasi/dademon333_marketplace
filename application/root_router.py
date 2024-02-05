from fastapi import APIRouter
from application.web.views.v1.acceptances import acceptance_router
from application.web.views.v1.discounts import discount_router
from application.web.views.v1.goods import good_router
from application.web.views.v1.postings import posting_router
from application.web.views.v1.sku import sku_router
from application.web.views.v1.tasks import task_router

root_router = APIRouter()

root_router.include_router(
    acceptance_router,
    tags=["Acceptances"],
)
root_router.include_router(
    discount_router,
    tags=["Discounts"],
)
root_router.include_router(
    good_router,
    tags=["Goods"],
)
root_router.include_router(
    posting_router,
    tags=["Postings"],
)
root_router.include_router(
    sku_router,
    tags=["SKU"],
)
root_router.include_router(
    task_router,
    tags=["Tasks"],
)
