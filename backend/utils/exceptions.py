from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError


async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Data conflict — duplicate or invalid reference.", "error": str(exc.orig)}
    )


async def operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database connection error. Please try again later."}
    )


async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error": str(exc)}
    )
