from __future__ import annotations

import functools
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setuptools_scm import get_version

from app.log_helper import init_logger as _init_logger

from .controllers import ALL_ROUTERS
from .settings import AppSettings
from .utils.fastapi import FASTAPI_RESPONSES, ErrorReportMiddleware

__version__ = get_version(root="..", relative_to=__file__)

logger = logging.getLogger(__name__)


def init_logger(app_settings: AppSettings) -> None:
    _init_logger(f"team3@{__version__}", app_settings)


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI(responses=FASTAPI_RESPONSES)

    app.add_event_handler(
        "startup", functools.partial(_web_app_startup, app, app_settings)
    )

    for api_router in ALL_ROUTERS:
        app.include_router(api_router)

    return app


async def _web_app_startup(app: FastAPI, app_settings: AppSettings) -> None:
    if app_settings.DEBUG_ALLOW_CORS_ALL_ORIGIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["x-total"],
        )
        logger.error("`DEBUG_ALLOW_CORS_ALL_ORIGIN` is on!")

    app.add_middleware(ErrorReportMiddleware)
