from typing import List
from fastapi import APIRouter, Depends, Path
from app.api.deps import get_telemetry_service
from app.models.intelligence import (
    TelemetryResponse,
    JobRoleRecord,
    ClusterPolicyResponse,
    NationalDeficitItem,
)
from app.services.telemetry_service import TelemetryService

router = APIRouter()

@router.get(
    "/telemetry",
    response_model=TelemetryResponse,
    summary="Mode 2: National Industry Telemetry Overview",
    description="Retrieve high-level macro skilling indicators, role demand distributions, and critical deficits."
)
async def get_telemetry_overview(
    telemetry_service: TelemetryService = Depends(get_telemetry_service)
):
    return telemetry_service.get_telemetry_overview()


@router.get(
    "/roles",
    response_model=List[JobRoleRecord],
    summary="Mode 2: Job Role Demand Dataset",
    description="Retrieve current dataset records with open roles, required top skills, and salaries."
)
async def get_role_demand_data(
    telemetry_service: TelemetryService = Depends(get_telemetry_service)
):
    return telemetry_service.get_role_records()


@router.get(
    "/clusters",
    response_model=List[str],
    summary="Mode 2: List Industrial Clusters",
    description="List active industrial clusters available for geospatial policy mapping."
)
async def get_supported_clusters(
    telemetry_service: TelemetryService = Depends(get_telemetry_service)
):
    return telemetry_service.get_available_clusters()


@router.get(
    "/cluster/{cluster_name}",
    response_model=ClusterPolicyResponse,
    summary="Mode 2: Regional Cluster Focus & Policy Intervention",
    description="Retrieve district-level skilling focus and recommended governmental intervention."
)
async def get_cluster_policy(
    cluster_name: str = Path(..., description="Name of the industrial cluster or district"),
    telemetry_service: TelemetryService = Depends(get_telemetry_service)
):
    return telemetry_service.get_cluster_policy(cluster_name)


@router.get(
    "/deficits",
    response_model=List[NationalDeficitItem],
    summary="Mode 2: Critical National Deficits",
    description="List major technical domains and their unmet industry demand percentage."
)
async def get_national_deficits(
    telemetry_service: TelemetryService = Depends(get_telemetry_service)
):
    return telemetry_service.get_national_deficits()
