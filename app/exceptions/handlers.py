from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.models import ErrorResponse
from .custom import AppException

async def app_exception_handler(request:Request,exc:AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.message,
            code=exc.status_code
        ).model_dump()
    )

async def http_exception_handler(request:Request,exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=exc.status_code
        ).model_dump()
    )