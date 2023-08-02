from fastapi import Request, status
from fastapi.responses import JSONResponse


async def default_error_handler(_: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error"},
    )
