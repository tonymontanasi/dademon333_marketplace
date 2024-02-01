from fastapi import APIRouter
from application.web.views.v1.acceptance import acceptance_router

root_router = APIRouter()

root_router.include_router(
    acceptance_router,
    tags=["Acceptances"],
)
