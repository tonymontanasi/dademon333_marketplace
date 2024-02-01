import logging.config

from fastapi import FastAPI

from application.middlewares.request_id import RequestIDMiddleware
from application.root_router import root_router
from application.utils.log_config import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)


def get_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(root_router)
    app_.add_middleware(RequestIDMiddleware)
    return app_


app = get_app()
