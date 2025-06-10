from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
import os

from app.core.config import settings
from app.api.v1.api import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.core.exceptions import CustomException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Check if we're running on Vercel
is_vercel = os.environ.get('VERCEL', '0') == '1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting FastAPI Backend...")
    
    # Only create tables if not on Vercel (use migrations instead for Vercel)
    if not is_vercel:
        from app.core.database import engine, Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down...")
    if not is_vercel:
        from app.core.redis import close_redis
        await close_redis()
    logger.info("✅ Cleanup completed")

def create_application() -> FastAPI:
    # Determine if running in production
    is_production = os.getenv("VERCEL_ENV") == "production" or os.getenv("ENVIRONMENT") == "production"
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A modern Python backend with MySQL, Redis, and essential libraries",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if not is_production else None,
        docs_url=f"{settings.API_V1_STR}/docs" if not is_production else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if not is_production else None,
        lifespan=lifespan
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Security middleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    
    # Only add rate limiting if not on Vercel (use Vercel's built-in rate limiting instead)
    if not is_vercel:
        app.add_middleware(RateLimitMiddleware, calls=100, period=60)

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Exception handlers
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": exc.error_code}
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": "Endpoint not found"}
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        logger.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
        
    # Add a simple root route for Vercel
    @app.get("/")
    async def root():
        return {"message": "Welcome to FastAPI Backend", "docs": f"{settings.API_V1_STR}/docs"}

    return app

app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=settings.DEBUG,
        log_level="info"
    )
