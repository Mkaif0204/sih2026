import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.services.gemini_service import gemini_service
from app.services.telemetry_service import telemetry_service

# Setup logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME}...")
    logger.info(f"Gemini configured: {gemini_service.is_configured}")
    logger.info(f"Loaded telemetry records: {len(telemetry_service.get_role_records())}")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=(
        "Production-ready FastAPI backend for SkillPulse AI (SIH26134), providing automated "
        "syllabus skill gap audits, national industry telemetry, and career trajectory mapping "
        "integrated with Indian government skilling programs."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def health_check():
    """System health check and operational status."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "gemini_configured": gemini_service.is_configured,
        "model": settings.GEMINI_MODEL,
        "telemetry_records": len(telemetry_service.get_role_records()),
    }

@app.get("/", tags=["System"])
async def root():
    """Root redirect / information endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_check": "/health",
    }
