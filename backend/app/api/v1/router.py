from fastapi import APIRouter
from app.api.v1.endpoints import gap_analysis, intelligence, recommendation

api_router = APIRouter()

api_router.include_router(
    gap_analysis.router,
    prefix="/gap-analysis",
    tags=["Mode 1: Syllabus Gap Analysis"]
)

api_router.include_router(
    intelligence.router,
    prefix="/intelligence",
    tags=["Mode 2: Industry Skill Intelligence"]
)

api_router.include_router(
    recommendation.router,
    prefix="/recommendations",
    tags=["Mode 3: Career Path & Recommendations"]
)
