# app/config/custom_exceptions.py
from typing import Any

from fastapi import HTTPException, Request, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.message = message


def custom_http_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": exc.message
        },
        headers=exc.headers
    )


def custom_validation_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


def custom_authentication_exception_handler(request: Request, exc: Any):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={
                "status": 401,
                "error": "Not authenticated"
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": exc.detail
        }
    )


def attribute_error_exception(request: Request, exc: Any):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "error": "Internal Server Error"
        }
    )


def custom_generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "error": "Internal Server Error"
        }
    )


class ExceptionHandlerRegistry:
    @staticmethod
    def register_exception_handlers(app: FastAPI):
        app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
        app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
        app.add_exception_handler(HTTPException, custom_authentication_exception_handler)
        app.add_exception_handler(AttributeError, attribute_error_exception)
        app.add_exception_handler(Exception, custom_generic_exception_handler)
