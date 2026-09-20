from pydantic import BaseModel, Field
from typing import List

class GapAnalysisRequest(BaseModel):
    target_role: str = Field(
        default="Software Engineer",
        description="Target job role for curriculum comparison",
        examples=["Software Engineer", "AI Engineer", "Cloud Architect"]
    )
    syllabus_text: str = Field(
        ...,
        description="Raw text of the academic curriculum or syllabus",
        min_length=5
    )

class GapAnalysisResponse(BaseModel):
    target_role: str = Field(..., description="The role evaluated against")
    alignment_score: int = Field(..., ge=0, le=100, description="Curriculum alignment score as percentage (0-100)")
    summary: str = Field(..., description="Executive summary of the alignment evaluation")
    verified_competencies: List[str] = Field(default_factory=list, description="List of verified academic competencies present in syllabus")
    critical_deficits: List[str] = Field(default_factory=list, description="List of identified critical industry deficits")
    raw_markdown: str = Field(..., description="Full formatted markdown output as rendered in the dashboard")
    source: str = Field(..., description="Origin of the response: 'gemini' or 'fallback'")
