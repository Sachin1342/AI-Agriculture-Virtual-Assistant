import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import chatbot_routes, prediction_routes
from app.core.config import settings
from app.db.database import SessionLocal, init_db
from app.db.seed import seed_all

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Driven Virtual Assistant for Crop Intelligence",
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database and seed data on startup."""
    try:
        init_db()
        logger.info("Database tables initialized")

        db = SessionLocal()
        try:
            seed_all(db)
        finally:
            db.close()
    except Exception:
        logger.exception("Database initialization error")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(chatbot_routes.router)
app.include_router(prediction_routes.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Crop Assistant AI",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }


@app.get("/api/v1")
async def api_info():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "endpoints": {
            "chatbot": "/api/v1/chatbot",
            "predictions": "/api/v1/predictions",
            "documentation": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
