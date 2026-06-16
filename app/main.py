from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.errors import RateLimitError, TaskValidationError


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version)
    app.include_router(router)

    @app.exception_handler(RateLimitError)
    async def rate_limit_handler(_: Request, exc: RateLimitError) -> JSONResponse:
        """Map concurrency limits to HTTP 429."""
        return JSONResponse(status_code=429, content={"detail": str(exc)})

    @app.exception_handler(TaskValidationError)
    async def validation_handler(_: Request, exc: TaskValidationError) -> JSONResponse:
        """Map request validation issues to HTTP 422."""
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    return app


app = create_app()
