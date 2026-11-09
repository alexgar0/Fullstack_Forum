from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):  # noqa: N818
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        print(f"Handling AppException: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "details": exc.details,
            },
        )


class NotFoundError(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=404, details=details)


class PermissionDeniedError(AppException):
    def __init__(
        self,
        message: str = "Permission denied",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=403, details=details)


class ExistingResourceError(AppException):
    def __init__(
        self,
        message: str = "Resource already exists",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=409, details=details)


class InvalidLengthError(AppException):
    def __init__(
        self,
        message: str = "Invalid content length",
        min_length: int | None = None,
        max_length: int | None = None,
        details: dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if min_length is not None:
            error_details["min_length"] = min_length
        if max_length is not None:
            error_details["max_length"] = max_length

        super().__init__(message, status_code=400, details=error_details)
