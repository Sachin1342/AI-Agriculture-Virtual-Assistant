from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api import chatbot_routes, prediction_routes
from app.db.database import init_db, SessionLocal
from app.db.seed import seed_all

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Driven Virtual Assistant for Crop Intelligence"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    try:
        init_db()
        print("✓ Database tables initialized")
        
        # Seed data
        db = SessionLocal()
        try:
            seed_all(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Database initialization error: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(chatbot_routes.router)
app.include_router(prediction_routes.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Crop Assistant AI",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }

@app.get("/api/v1")
async def api_info():
    """API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "endpoints": {
            "chatbot": "/api/v1/chatbot",
            "predictions": "/api/v1/predictions",
            "documentation": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
