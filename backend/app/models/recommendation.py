from pydantic import BaseModel, Field
from typing import List

class CareerTrajectoryRequest(BaseModel):
    current_skills: str = Field(
        default="html, css, python basics",
        description="Candidate's current skills (comma-separated)",
        examples=["html, css, python basics", "c++, data structures, sql"]
    )
    target_career: str = Field(
        default="Full Stack Developer",
        description="Target career track or job role",
        examples=["Full Stack Developer", "AI Engineer", "Cloud Architect"]
    )

class GovernmentPathway(BaseModel):
    provider: str = Field(..., description="Government entity or initiative, e.g., NASSCOM FutureSkills Prime, Skill India Digital")
    program: str = Field(..., description="Recommended program, certification, or domain curriculum")

class CareerTrajectoryResponse(BaseModel):
    target_career: str
    current_skills: str
    employability_match: int = Field(..., ge=0, le=100, description="Employability match score as percentage")
    summary: str = Field(..., description="Assessment summary of candidate readiness")
    technical_deficits: List[str] = Field(default_factory=list, description="Specific identified technical shortcomings")
    government_pathways: List[GovernmentPathway] = Field(default_factory=list, description="Directly mapped Indian government training initiatives")
    raw_markdown: str = Field(..., description="Full formatted markdown output as rendered in the dashboard")
    source: str = Field(..., description="Origin of the response: 'gemini' or 'fallback'")
