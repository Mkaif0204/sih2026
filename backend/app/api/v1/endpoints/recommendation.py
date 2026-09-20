from fastapi import APIRouter, Depends
from app.api.deps import get_gemini_service
from app.models.recommendation import CareerTrajectoryRequest, CareerTrajectoryResponse
from app.services.gemini_service import GeminiService

router = APIRouter()

@router.post(
    "/trajectory",
    response_model=CareerTrajectoryResponse,
    summary="Mode 3: Personalized Learning Trajectory & Indian Govt Pathways",
    description="Maps a candidate's current skill profile against a target role, identifying deficits and pointing to real Indian skilling programs."
)
async def generate_career_trajectory(
    payload: CareerTrajectoryRequest,
    gemini_service: GeminiService = Depends(get_gemini_service),
):
    return gemini_service.generate_career_trajectory(
        current_skills=payload.current_skills,
        target_career=payload.target_career
    )
