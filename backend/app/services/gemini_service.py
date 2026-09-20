import logging
import re
from typing import List, Tuple
import google.generativeai as genai

from app.core.config import settings
from app.models.gap_analysis import GapAnalysisResponse
from app.models.recommendation import CareerTrajectoryResponse, GovernmentPathway

logger = logging.getLogger(__name__)

FALLBACK_GAP_MARKDOWN = """### 🎯 Alignment Score: 52%
The curriculum covers traditional theoretical fundamentals well, but lacks modern distributed development workflows and containerization standards.

#### ✅ Verified Academic Competencies
* Core Data Structures & Algorithms implementation in C++.
* Relational Schema Normalization and SQL with MySQL.
* Object-Oriented Software Design fundamentals in Java.

#### ❌ Critical Industry Deficits
* Version Control Workflows (Git, GitHub Enterprise).
* Modern Frameworks (React.js, FastAPI, Node.js).
* Containerization & Cloud Infrastructure (Docker, AWS)."""

FALLBACK_TRAJECTORY_MARKDOWN = """### 🚀 Employability Match: 65%
The candidate possesses fundamental programming syntax but needs structured backend framework experience and database administration skills to achieve enterprise readiness.

#### ❌ Technical Deficits
* Full-Stack Web Frameworks (React.js, Node.js or FastAPI).
* Production Database Engineering (PostgreSQL, Schema Migrations).
* Automated Testing & Version Control (Git, CI/CD).

#### 🏛️ Government Pathways
* **NASSCOM FutureSkills Prime:** Full Stack Web Developer Certification Track.
* **Skill India Digital (PMKVY 4.0):** Advanced Application Development & Cloud Deployment Program."""


class GeminiService:
    """Service encapsulating Gemini API prompt execution, score parsing, and fallback handling."""

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        self._configured = False
        self._init_client()

    def _init_client(self):
        if self.api_key and self.api_key.strip():
            try:
                genai.configure(api_key=self.api_key.strip())
                self._configured = True
                logger.info(f"GeminiService configured with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to configure Gemini client: {e}")
                self._configured = False
        else:
            logger.warning("GeminiService initialized without API key. Offline fallbacks will be used.")
            self._configured = False

    @property
    def is_configured(self) -> bool:
        return self._configured

    @staticmethod
    def extract_score(text: str, default: int = 55) -> int:
        """Extract percentage score from text (e.g. '52%' -> 52)."""
        match = re.search(r'(\d+)%', text)
        if match:
            try:
                score = int(match.group(1))
                return max(0, min(100, score))
            except ValueError:
                pass
        return default

    @staticmethod
    def _parse_bullet_list(text_block: str) -> List[str]:
        """Extract clean strings from markdown bullets (* or -)."""
        items = []
        for line in text_block.splitlines():
            cleaned = line.strip()
            if cleaned.startswith("* ") or cleaned.startswith("- "):
                val = cleaned[2:].strip()
                # Remove bold markers if pure bullet item
                val = re.sub(r'^\*\*(.*?)\*\*$', r'\1', val)
                if val:
                    items.append(val)
        return items

    def _parse_gap_analysis_output(self, raw_text: str, target_role: str, source: str) -> GapAnalysisResponse:
        score = self.extract_score(raw_text, default=52)

        # Extract summary sentence
        summary = "Curriculum covers fundamentals but shows gaps against modern industry demands."
        summary_match = re.search(r'###\s*🎯\s*Alignment Score:[^\n]*\n+([^\n#]+)', raw_text)
        if summary_match and summary_match.group(1).strip():
            summary = summary_match.group(1).strip()

        # Extract verified competencies
        verified_competencies = []
        comp_match = re.search(
            r'####\s*✅\s*Verified Academic Competencies\s*\n(.*?)(?=####|\Z)',
            raw_text,
            re.DOTALL
        )
        if comp_match:
            verified_competencies = self._parse_bullet_list(comp_match.group(1))

        if not verified_competencies:
            verified_competencies = [
                "Core Data Structures & Algorithms implementation in C++.",
                "Relational Schema Normalization and SQL with MySQL.",
                "Object-Oriented Software Design fundamentals in Java."
            ]

        # Extract critical deficits
        critical_deficits = []
        deficit_match = re.search(
            r'####\s*❌\s*Critical Industry Deficits\s*\n(.*?)(?=####|\Z)',
            raw_text,
            re.DOTALL
        )
        if deficit_match:
            critical_deficits = self._parse_bullet_list(deficit_match.group(1))

        if not critical_deficits:
            critical_deficits = [
                "Version Control Workflows (Git, GitHub Enterprise).",
                "Modern Frameworks (React.js, FastAPI, Node.js).",
                "Containerization & Cloud Infrastructure (Docker, AWS)."
            ]

        return GapAnalysisResponse(
            target_role=target_role,
            alignment_score=score,
            summary=summary,
            verified_competencies=verified_competencies,
            critical_deficits=critical_deficits,
            raw_markdown=raw_text.strip(),
            source=source
        )

    def _parse_trajectory_output(
        self, raw_text: str, current_skills: str, target_career: str, source: str
    ) -> CareerTrajectoryResponse:
        score = self.extract_score(raw_text, default=65)

        # Extract summary
        summary = "Candidate demonstrates good initial foundation but requires structured framework exposure."
        summary_match = re.search(r'###\s*🚀\s*Employability Match:[^\n]*\n+([^\n#]+)', raw_text)
        if summary_match and summary_match.group(1).strip():
            summary = summary_match.group(1).strip()

        # Extract technical deficits
        technical_deficits = []
        deficits_match = re.search(
            r'####\s*❌\s*Technical Deficits\s*\n(.*?)(?=####|\Z)',
            raw_text,
            re.DOTALL
        )
        if deficits_match:
            technical_deficits = self._parse_bullet_list(deficits_match.group(1))

        if not technical_deficits:
            technical_deficits = [
                "Full-Stack Web Frameworks (React.js, Node.js or FastAPI).",
                "Production Database Engineering (PostgreSQL, Schema Migrations).",
                "Automated Testing & Version Control (Git, CI/CD)."
            ]

        # Extract government pathways
        government_pathways: List[GovernmentPathway] = []
        gov_match = re.search(
            r'####\s*🏛️\s*Government (?:Training )?Pathways\s*\n(.*?)(?=####|\Z)',
            raw_text,
            re.DOTALL
        )
        if gov_match:
            for line in gov_match.group(1).splitlines():
                line = line.strip()
                if line.startswith("* ") or line.startswith("- "):
                    line = line[2:].strip()
                    # e.g. **NASSCOM FutureSkills Prime:** Full Stack Track
                    m = re.match(r'\*\*(.*?):\*\*\s*(.*)', line)
                    if m:
                        government_pathways.append(GovernmentPathway(
                            provider=m.group(1).strip(),
                            program=m.group(2).strip()
                        ))
                    else:
                        government_pathways.append(GovernmentPathway(
                            provider="Skill India Digital",
                            program=line
                        ))

        if not government_pathways:
            government_pathways = [
                GovernmentPathway(
                    provider="NASSCOM FutureSkills Prime",
                    program="Full Stack Web Developer Certification Track."
                ),
                GovernmentPathway(
                    provider="Skill India Digital (PMKVY 4.0)",
                    program="Advanced Application Development & Cloud Deployment Program."
                )
            ]

        return CareerTrajectoryResponse(
            target_career=target_career,
            current_skills=current_skills,
            employability_match=score,
            summary=summary,
            technical_deficits=technical_deficits,
            government_pathways=government_pathways,
            raw_markdown=raw_text.strip(),
            source=source
        )

    def audit_curriculum(self, syllabus_text: str, target_role: str = "Software Engineer") -> GapAnalysisResponse:
        """Run Mode 1 Syllabus Skill Gap Analysis."""
        if not self._configured:
            logger.info("Gemini not configured; returning baseline audit.")
            return self._parse_gap_analysis_output(FALLBACK_GAP_MARKDOWN, target_role, source="fallback")

        prompt = f"""
You are an academic curriculum auditor for the Government of India.
Analyze this syllabus text:
{syllabus_text[:4000]}

Target Role: {target_role}

Provide your assessment in this exact layout:
### 🎯 Alignment Score: [Score]%
[1 concise, professional sentence summarizing curriculum relevance.]

#### ✅ Verified Academic Competencies
* [Module 1 present in syllabus]
* [Module 2 present in syllabus]
* [Module 3 present in syllabus]

#### ❌ Critical Industry Deficits
* [Missing modern tool/framework 1]
* [Missing modern tool/framework 2]
* [Missing modern tool/framework 3]
"""
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return self._parse_gap_analysis_output(response.text, target_role, source="gemini")
            else:
                logger.warning("Empty response from Gemini; falling back.")
                return self._parse_gap_analysis_output(FALLBACK_GAP_MARKDOWN, target_role, source="fallback")
        except Exception as err:
            logger.error(f"Gemini API call error during audit_curriculum: {err}")
            return self._parse_gap_analysis_output(FALLBACK_GAP_MARKDOWN, target_role, source="fallback")

    def generate_career_trajectory(
        self, current_skills: str, target_career: str = "Full Stack Developer"
    ) -> CareerTrajectoryResponse:
        """Run Mode 3 Career Path & Skill Recommendation."""
        if not self._configured:
            logger.info("Gemini not configured; returning baseline trajectory.")
            return self._parse_trajectory_output(FALLBACK_TRAJECTORY_MARKDOWN, current_skills, target_career, source="fallback")

        prompt = f"""
You are a technical career pathway advisor for the Government of India.
Candidate Current Skills: {current_skills}
Candidate Target Role: {target_career}

Strict constraint: Recommend ONLY real Indian government skilling programs (such as PMKVY 4.0, NASSCOM FutureSkills Prime, SWAYAM/NPTEL, or NIELIT). Never cite foreign programs.

Provide your assessment in this exact layout:
### 🚀 Employability Match: [Score]%
[1 concise, professional sentence summarizing readiness without markdown formatting.]

#### ❌ Technical Deficits
* [Concrete technical deficiency 1]
* [Concrete technical deficiency 2]
* [Concrete technical deficiency 3]

#### 🏛️ Government Training Pathways
* **NASSCOM FutureSkills Prime:** [Course or track title targeting gap]
* **Skill India Digital (PMKVY 4.0):** [Certification or domain curriculum]
"""
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return self._parse_trajectory_output(response.text, current_skills, target_career, source="gemini")
            else:
                logger.warning("Empty response from Gemini; falling back.")
                return self._parse_trajectory_output(FALLBACK_TRAJECTORY_MARKDOWN, current_skills, target_career, source="fallback")
        except Exception as err:
            logger.error(f"Gemini API call error during generate_career_trajectory: {err}")
            return self._parse_trajectory_output(FALLBACK_TRAJECTORY_MARKDOWN, current_skills, target_career, source="fallback")

gemini_service = GeminiService()
