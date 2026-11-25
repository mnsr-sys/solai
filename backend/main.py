from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

StateCode = Literal["Telangana", "Karnataka"]

STATE_CONFIG = {
    "Telangana": {
        "code": "TS",
        "priority": 1,
        "pilot_status": "primary-demo-state",
        "districts": [
            "Hyderabad", "Medchal-Malkajgiri", "Rangareddy", "Sangareddy",
            "Yadadri Bhuvanagiri", "Warangal", "Karimnagar", "Nalgonda",
        ],
        "data_notice": "District list is an initial demo selector, not a verified inventory of substations or candidate parcels.",
    },
    "Karnataka": {
        "code": "KA",
        "priority": 2,
        "pilot_status": "next-expansion-state",
        "districts": [
            "Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Tumakuru",
            "Belagavi", "Dharwad", "Kalaburagi", "Dakshina Kannada",
        ],
        "data_notice": "District list is an initial demo selector, not a verified inventory of substations or candidate parcels.",
    },
}

app = FastAPI(
    title="Reker SolAI API",
    version="0.2.0",
    description="Multi-state solar substation screening; Telangana is the first implementation priority, followed by Karnataka.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

METHODOLOGY_VERSION = "screening-v0.2"
projects: dict[str, dict] = {}


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    district: str = Field(min_length=2, max_length=80)
    state: StateCode = "Telangana"
    data_status: Literal["public", "synthetic", "utility-provided"] = "synthetic"


class SiteFeatures(BaseModel):
    site_id: str = Field(min_length=1, max_length=80)
    label: str = Field(min_length=1, max_length=120)
    usable_area_m2: float = Field(ge=0)
    land_availability: float = Field(ge=0, le=100, description="0-100 suitability score")
    shading: float = Field(ge=0, le=100, description="0-100; higher means less shading")
    slope: float = Field(ge=0, le=100, description="0-100; higher means more suitable slope")
    flood_safety: float = Field(ge=0, le=100, description="0-100; higher means lower flood risk")
    grid_proximity: float = Field(ge=0, le=100, description="0-100 proximity screening score")
    data_status: Literal["public", "synthetic", "utility-provided"] = "synthetic"


class ScreeningRequest(BaseModel):
    state: StateCode = "Telangana"
    district: str = Field(default="Hyderabad", min_length=2, max_length=80)
    sites: list[SiteFeatures] = Field(min_length=1, max_length=500)
    weights: dict[str, float] | None = None

    @model_validator(mode="after")
    def validate_weights(self):
        if self.weights is not None:
            required = {"land_availability", "shading", "slope", "flood_safety", "grid_proximity"}
            if set(self.weights) != required:
                raise ValueError(f"Weights must contain exactly: {sorted(required)}")
            if any(v < 0 for v in self.weights.values()) or sum(self.weights.values()) <= 0:
                raise ValueError("Weights must be non-negative and sum to a positive value")
        return self


class SolarEstimateRequest(BaseModel):
    usable_area_m2: float = Field(gt=0)
    installed_density_w_per_m2: float = Field(default=200, gt=0, le=400)
    specific_yield_mwh_per_mw_year: float = Field(default=1500, gt=0, le=3000)
    grid_emission_factor_tco2e_per_mwh: float = Field(gt=0, le=2, description="User-supplied, sourced factor")


DEFAULT_WEIGHTS = {
    "land_availability": 0.30,
    "shading": 0.20,
    "slope": 0.15,
    "flood_safety": 0.20,
    "grid_proximity": 0.15,
}


@app.get("/")
def root():
    return {"product": "Reker SolAI", "version": app.version, "status": "prototype"}


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/v1/states")
def list_states():
    return {
        "priority_order": ["Telangana", "Karnataka"],
        "default_state": "Telangana",
        "states": STATE_CONFIG,
        "notice": "State and district selectors are geographic scaffolding. They do not imply verified substation or land datasets.",
    }


@app.post("/api/v1/projects", status_code=201)
def create_project(payload: ProjectCreate):
    if payload.district not in STATE_CONFIG[payload.state]["districts"]:
        raise HTTPException(status_code=422, detail=f"District is not in the current {payload.state} demo selector.")
    project_id = str(uuid4())
    record = {
        "project_id": project_id,
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "screening",
        "methodology_version": METHODOLOGY_VERSION,
    }
    projects[project_id] = record
    return record


@app.get("/api/v1/projects")
def list_projects():
    return list(projects.values())


@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


@app.post("/api/v1/sites/score")
def score_sites(payload: ScreeningRequest):
    if payload.district not in STATE_CONFIG[payload.state]["districts"]:
        raise HTTPException(status_code=422, detail=f"District is not in the current {payload.state} demo selector.")
    weights = payload.weights or DEFAULT_WEIGHTS
    total_weight = sum(weights.values())
    normalized = {key: value / total_weight for key, value in weights.items()}
    results = []
    for site in payload.sites:
        features = site.model_dump()
        score = sum(features[key] * normalized[key] for key in normalized)
        results.append({
            **features,
            "suitability_score": round(score, 2),
            "screening_band": "High" if score >= 75 else "Medium" if score >= 50 else "Low",
            "methodology_version": METHODOLOGY_VERSION,
            "validation_status": "not-utility-validated",
            "limitations": [
                "Screening score is not an engineering approval.",
                "Grid proximity does not establish electrical hosting capacity.",
            ],
        })
    results.sort(key=lambda item: item["suitability_score"], reverse=True)
    return {
        "state": payload.state,
        "district": payload.district,
        "methodology_version": METHODOLOGY_VERSION,
        "weights": normalized,
        "ranked_sites": results,
        "notice": "Scores are indicative screening results. Validate source data and site conditions with the utility.",
    }


@app.post("/api/v1/solar/estimate")
def estimate_solar(payload: SolarEstimateRequest):
    capacity_mw_dc = payload.usable_area_m2 * payload.installed_density_w_per_m2 / 1_000_000
    annual_generation_mwh = capacity_mw_dc * payload.specific_yield_mwh_per_mw_year
    avoided_tco2e = annual_generation_mwh * payload.grid_emission_factor_tco2e_per_mwh
    return {
        "usable_area_m2": payload.usable_area_m2,
        "installed_density_w_per_m2": payload.installed_density_w_per_m2,
        "estimated_capacity_mw_dc": round(capacity_mw_dc, 4),
        "specific_yield_mwh_per_mw_year": payload.specific_yield_mwh_per_mw_year,
        "estimated_annual_generation_mwh": round(annual_generation_mwh, 2),
        "grid_emission_factor_tco2e_per_mwh": payload.grid_emission_factor_tco2e_per_mwh,
        "estimated_avoided_emissions_tco2e_per_year": round(avoided_tco2e, 2),
        "methodology_version": METHODOLOGY_VERSION,
        "validation_status": "indicative-not-verified",
        "notice": "Supply a documented grid factor. Estimates are not verified carbon credits or utility approvals.",
    }
