from __future__ import annotations

import dataclasses
import logging
from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class _ManagedError(Exception):
    code: str
    message: str
    detail: dict[str, Any] | None = None


class AuthError(_ManagedError):
    pass


class LogicError(_ManagedError):
    pass


class _ErrorResponseModel(BaseModel):
    class ErrorDetail(BaseModel):
        code: str
        message: str
        detail: Optional[Dict[str, Any]] = None

    detail: _ErrorResponseModel.ErrorDetail

    @staticmethod
    def from_exc(exc: _ManagedError) -> _ErrorResponseModel:
        return _ErrorResponseModel(
            detail=_ErrorResponseModel.ErrorDetail(
                code=exc.code,
                message=exc.message,
                detail=exc.detail,
            ),
        )


_ErrorResponseModel.update_forward_refs()


FASTAPI_RESPONSES: dict[int | str, dict[str, Any]] = {
    403: {
        "description": "Auth Error",
        "model": _ErrorResponseModel,
    },
    409: {
        "description": "Logical error",
        "model": _ErrorResponseModel,
    },
    500: {
        "description": "Server error",
        "model": _ErrorResponseModel,
    },
}


class ErrorReportMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        response_started = False

        async def _send(message: Message) -> None:
            nonlocal response_started

            if message["type"] == "http.response.start":
                response_started = True

            await send(message)

        try:
            await self.app(scope, receive, _send)
            return

        except AuthError as err:
            err_response = JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=_ErrorResponseModel.from_exc(err).dict(),
            )
        except LogicError as err:
            err_response = JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=_ErrorResponseModel.from_exc(err).dict(),
            )
        except Exception:
            logger.exception("Internal server error")

            err_response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=_ErrorResponseModel(
                    detail=_ErrorResponseModel.ErrorDetail(
                        code="server_error",
                        message="unexpected server error",
                    )
                ).dict(),
            )

        if not response_started:
            await err_response(scope, receive, send)


async def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-FORWARDED-FOR")
    return (  # type: ignore
        (x_forwarded_for.split(",")[0]).split(":")[0]
        if x_forwarded_for
        else request.client.host  # type: ignore
    )
