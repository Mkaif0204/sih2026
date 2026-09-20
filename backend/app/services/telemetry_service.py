import os
import logging
from pathlib import Path
from typing import List, Optional
import pandas as pd

from app.core.config import settings
from app.models.intelligence import (
    MetricOverview,
    MetricItem,
    JobRoleRecord,
    NationalDeficitItem,
    ClusterPolicyResponse,
    TelemetryResponse,
)

logger = logging.getLogger(__name__)

FALLBACK_DATA = {
    "Job_Role": ["AI Engineer", "Full Stack Dev", "Cloud Architect", "Data Analyst", "Cybersecurity Analyst", "Blockchain Dev"],
    "Top_Skill": ["GenAI / PyTorch", "Next.js / React", "Kubernetes / AWS", "Pandas / SQL", "Zero Trust", "Solidity / Web3"],
    "Avg_Salary_LPA": [18.5, 12.0, 22.0, 8.5, 15.0, 16.0],
    "Open_Roles": [1240, 3500, 890, 2100, 1100, 450],
    "Growth_Projected_2026_Pct": [92, 85, 88, 75, 90, 82]
}

CLUSTERS = [
    "Hyderabad (Telangana)",
    "Bengaluru (Karnataka)",
    "Pune (Maharashtra)",
    "Chennai (Tamil Nadu)",
    "Noida (UP)"
]

NATIONAL_DEFICITS = [
    NationalDeficitItem(domain="Cloud Security Architecture", unmet_percentage=82),
    NationalDeficitItem(domain="Distributed Systems (Go/Rust)", unmet_percentage=74),
    NationalDeficitItem(domain="Applied MLOps Pipelines", unmet_percentage=68),
    NationalDeficitItem(domain="Embedded Firmware (IoT)", unmet_percentage=59),
]


class TelemetryService:
    """Service providing industry telemetry data, metrics, and regional policy lookups."""

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path or settings.DATA_CSV_PATH)
        self._df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self):
        """Loads dataset from CSV file or builds fallback dataframe."""
        if self.data_path.exists():
            try:
                self._df = pd.read_csv(self.data_path)
                logger.info(f"Loaded telemetry dataset from {self.data_path} with {len(self._df)} records.")
                return
            except Exception as e:
                logger.warning(f"Error reading CSV at {self.data_path}: {e}")

        # Check in project root if not found
        alt_path = Path(__file__).resolve().parent.parent.parent.parent / "industry_data.csv"
        if alt_path.exists():
            try:
                self._df = pd.read_csv(alt_path)
                logger.info(f"Loaded telemetry dataset from alternative path {alt_path}")
                return
            except Exception as e:
                logger.warning(f"Error reading alternative CSV {alt_path}: {e}")

        logger.info("Using embedded fallback telemetry dataset.")
        self._df = pd.DataFrame(FALLBACK_DATA)

    def get_role_records(self) -> List[JobRoleRecord]:
        """Return list of validated job role demand records."""
        if self._df is None or self._df.empty:
            self._load_data()

        records = []
        for _, row in self._df.iterrows():
            record = JobRoleRecord(
                job_role=str(row["Job_Role"]),
                top_skill=str(row["Top_Skill"]),
                avg_salary_lpa=float(row["Avg_Salary_LPA"]),
                open_roles=int(row["Open_Roles"]),
                growth_projected_2026_pct=int(row.get("Growth_Projected_2026_Pct", 80))
            )
            records.append(record)
        return records

    def get_metrics(self) -> MetricOverview:
        """Return macro national metrics."""
        return MetricOverview(
            high_demand_skills=MetricItem(label="High-Demand Skills", value="186", delta="↑ 12.4% MoM"),
            identified_deficits=MetricItem(label="Identified Deficits", value="72", delta="↓ 4.8% YoY"),
            indexed_syllabi=MetricItem(label="Indexed Syllabi", value="128", delta="Active Nodes"),
            emerging_vectors=MetricItem(label="Emerging Vectors", value="34", delta="Industry 4.0"),
        )

    def get_national_deficits(self) -> List[NationalDeficitItem]:
        """Return critical national deficit percentage list."""
        return NATIONAL_DEFICITS

    def get_available_clusters(self) -> List[str]:
        """Return list of supported industrial districts/clusters."""
        return CLUSTERS

    def get_cluster_policy(self, cluster_name: str) -> ClusterPolicyResponse:
        """Return localized cluster focus and recommended policy intervention."""
        clean_name = cluster_name.strip()
        if "Hyderabad" in clean_name:
            focus = "High concentration of Pharma-Tech, Cloud & Enterprise AI."
            intervention = "Expand AICTE-approved Applied Data Science intake by 35%."
        elif "Bengaluru" in clean_name:
            focus = "High concentration of DeepTech, Aerospace R&D & SaaS Startups."
            intervention = "Scale industry mentorship pipelines with local technology incubators."
        else:
            focus = f"High demand for Full-Stack, Embedded Systems & Cloud in {clean_name}."
            intervention = "Fund regional university Centers of Excellence in Cloud Architecture."

        return ClusterPolicyResponse(
            cluster_name=clean_name,
            cluster_focus=focus,
            policy_intervention=intervention
        )

    def get_telemetry_overview(self) -> TelemetryResponse:
        """Return unified telemetry response containing metrics, roles, and deficits."""
        return TelemetryResponse(
            metrics=self.get_metrics(),
            roles=self.get_role_records(),
            national_deficits=self.get_national_deficits(),
            available_clusters=self.get_available_clusters(),
        )

telemetry_service = TelemetryService()
