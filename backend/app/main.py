from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.config import settings
from app.utils.logger import get_logger

# Ensure agent tool registry is initialized before processing requests.
import app.tools.registry  # noqa: F401

logger = get_logger(__name__)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error for request %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_code": "validation_error",
            "message": "Payload validation failed.",
            "details": exc.errors(),
        },
    )


@app.get("/healthz")
async def healthz() -> dict:
    return {"success": True, "message": "OK"}


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting SenAI CRM app in %s mode.", settings.environment)
