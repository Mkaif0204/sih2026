from pydantic import BaseModel, Field
from typing import List

class MetricItem(BaseModel):
    label: str
    value: str
    delta: str

class MetricOverview(BaseModel):
    high_demand_skills: MetricItem = Field(
        default_factory=lambda: MetricItem(label="High-Demand Skills", value="186", delta="↑ 12.4% MoM")
    )
    identified_deficits: MetricItem = Field(
        default_factory=lambda: MetricItem(label="Identified Deficits", value="72", delta="↓ 4.8% YoY")
    )
    indexed_syllabi: MetricItem = Field(
        default_factory=lambda: MetricItem(label="Indexed Syllabi", value="128", delta="Active Nodes")
    )
    emerging_vectors: MetricItem = Field(
        default_factory=lambda: MetricItem(label="Emerging Vectors", value="34", delta="Industry 4.0")
    )

class JobRoleRecord(BaseModel):
    job_role: str
    top_skill: str
    avg_salary_lpa: float
    open_roles: int
    growth_projected_2026_pct: int

class NationalDeficitItem(BaseModel):
    domain: str
    unmet_percentage: int

class ClusterPolicyResponse(BaseModel):
    cluster_name: str
    cluster_focus: str
    policy_intervention: str

class TelemetryResponse(BaseModel):
    metrics: MetricOverview
    roles: List[JobRoleRecord]
    national_deficits: List[NationalDeficitItem]
    available_clusters: List[str]
