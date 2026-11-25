from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator
import httpx

DISTRICTS = [
    "Adilabad", "Bhadradri Kothagudem", "Hanamkonda", "Hyderabad",
    "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal",
    "Kamareddy", "Karimnagar", "Khammam", "Kumuram Bheem Asifabad",
    "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak",
    "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda",
    "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
    "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet",
    "Suryapet", "Vikarabad", "Wanaparthy", "Warangal",
    "Yadadri Bhuvanagiri",
]

app = FastAPI(
    title="Reker SolAI API",
    version="1.0.0",
    description="Telangana solar asset intelligence, generation monitoring and carbon MRV readiness API.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


DEFAULT_SCREENING_WEIGHTS = {
    "land_availability": 0.30,
    "shading": 0.20,
    "slope": 0.15,
    "flood_safety": 0.20,
    "grid_proximity": 0.15,
}

class CandidateSite(BaseModel):
    site_id: str = Field(min_length=1, max_length=80)
    label: str = Field(min_length=1, max_length=120)
    usable_area_m2: float = Field(ge=0)
    land_availability: float = Field(ge=0, le=100)
    shading: float = Field(ge=0, le=100, description="Higher means less shading")
    slope: float = Field(ge=0, le=100, description="Higher means more suitable terrain")
    flood_safety: float = Field(ge=0, le=100, description="Higher means lower flood exposure")
    grid_proximity: float = Field(ge=0, le=100, description="Proximity screening score only")
    data_status: Literal["public", "synthetic", "owner-provided", "utility-provided"] = "synthetic"

class SiteScreeningRequest(BaseModel):
    district: str
    sites: list[CandidateSite] = Field(min_length=1, max_length=500)
    weights: dict[str, float] | None = None

    @model_validator(mode="after")
    def validate_weights(self):
        if self.weights is not None:
            required = set(DEFAULT_SCREENING_WEIGHTS)
            if set(self.weights) != required:
                raise ValueError(f"Weights must contain exactly: {sorted(required)}")
            if any(v < 0 for v in self.weights.values()) or sum(self.weights.values()) <= 0:
                raise ValueError("Weights must be non-negative and sum to a positive value")
        return self

class SolarPotentialRequest(BaseModel):
    usable_area_m2: float = Field(gt=0)
    installed_density_w_per_m2: float = Field(default=200, gt=0, le=400)
    specific_yield_mwh_per_mw_year: float = Field(default=1500, gt=0, le=3000)
    grid_emission_factor_tco2e_per_mwh: float | None = Field(default=None, gt=0, le=2)

# Demo persistence only. Replace with managed PostgreSQL/PostGIS before production use.
projects: dict[str, dict] = {}
meter_readings: dict[str, list[dict]] = {}
audit_events: list[dict] = []

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    district: str
    asset_type: Literal["ground-mounted", "rooftop", "floating", "hybrid"] = "ground-mounted"
    capacity_mw: float = Field(gt=0, le=10000)
    latitude: float = Field(ge=15.0, le=20.5)
    longitude: float = Field(ge=77.0, le=82.0)
    substation_name: str | None = Field(default=None, max_length=160)
    owner: str | None = Field(default=None, max_length=160)
    commissioning_date: str | None = None
    data_status: Literal["synthetic", "owner-provided", "utility-provided"] = "synthetic"

class MeterReading(BaseModel):
    timestamp: datetime
    energy_mwh: float = Field(ge=0)
    meter_id: str = Field(min_length=1, max_length=100)
    reading_type: Literal["generation", "grid-export"] = "generation"
    source: str = Field(default="manual-upload", max_length=100)

class MeterBatch(BaseModel):
    readings: list[MeterReading] = Field(min_length=1, max_length=50000)

class MRVRequest(BaseModel):
    grid_emission_factor_tco2e_per_mwh: float = Field(gt=0, le=2)
    factor_source: str = Field(min_length=3, max_length=300)
    factor_vintage: str = Field(min_length=4, max_length=20)
    project_emissions_tco2e: float = Field(default=0, ge=0)
    leakage_tco2e: float = Field(default=0, ge=0)
    eligible_energy_basis: Literal["generation", "grid-export"] = "generation"
    methodology_name: str = Field(default="Indicative grid-displacement screening", max_length=200)

def log_event(entity_type: str, entity_id: str, action: str, details: dict):
    audit_events.append({
        "event_id": str(uuid4()), "entity_type": entity_type, "entity_id": entity_id,
        "action": action, "details": details,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

@app.get("/")
def root():
    return {"product": "Reker SolAI", "version": app.version, "status": "demo-ready", "geography": "Telangana"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat(), "geography": "Telangana"}

@app.get("/api/v1/states")
def list_states():
    return {
        "default_state": "Telangana",
        "states": {"Telangana": {"code": "TS", "districts": DISTRICTS}},
        "notice": "Telangana-only build. Districts are administrative selectors, not proof of asset or utility coverage.",
    }

@app.get("/api/v1/dashboard")
def dashboard():
    readings = [r for rows in meter_readings.values() for r in rows]
    generation = sum(r["energy_mwh"] for r in readings if r["reading_type"] == "generation")
    exports = sum(r["energy_mwh"] for r in readings if r["reading_type"] == "grid-export")
    return {
        "geography": "Telangana", "projects_registered": len(projects),
        "meter_records": len(readings), "generation_mwh": round(generation, 3),
        "grid_export_mwh": round(exports, 3),
        "estimated_avoided_emissions_tco2e": None,
        "data_notice": "Only uploaded records in this running demo instance are counted. No live utility feed is connected.",
    }


@app.post("/api/v1/sites/score")
def score_candidate_sites(payload: SiteScreeningRequest):
    if payload.district not in DISTRICTS:
        raise HTTPException(status_code=422, detail="District must be in Telangana.")
    weights = payload.weights or DEFAULT_SCREENING_WEIGHTS
    total = sum(weights.values())
    normalised = {k: v / total for k, v in weights.items()}
    ranked = []
    for site in payload.sites:
        values = site.model_dump()
        score = sum(values[k] * normalised[k] for k in normalised)
        ranked.append({
            **values,
            "suitability_score": round(score, 2),
            "screening_band": "High" if score >= 75 else "Medium" if score >= 50 else "Low",
            "status": "indicative-geospatial-screening",
            "limitations": [
                "Score is a prioritisation aid, not a land-title, engineering or statutory approval.",
                "Grid proximity does not establish feeder connectivity, spare hosting capacity or evacuation feasibility.",
                "Land, water, flood, slope and land-cover attributes require source-specific validation.",
            ],
        })
    ranked.sort(key=lambda x: x["suitability_score"], reverse=True)
    return {
        "state": "Telangana", "district": payload.district,
        "weights": normalised, "ranked_sites": ranked,
        "notice": "Candidate-site screening only. Confirm parcels, exclusions and grid feasibility with authoritative agencies and utilities.",
    }



@app.get("/api/v1/solar/resource")
def solar_resource(
    lat: float = Query(..., ge=15.0, le=20.5),
    lon: float = Query(..., ge=77.0, le=82.0),
    start: str = "20250101",
    end: str = "20251231",
    performance_ratio: float = Query(0.78, ge=0.5, le=0.9),
):
    """Fetch daily all-sky surface solar irradiation from NASA POWER for a Telangana point."""
    import re
    if not re.fullmatch(r"\\d{8}", start) or not re.fullmatch(r"\\d{8}", end) or start > end:
        raise HTTPException(status_code=422, detail="start/end must be ordered YYYYMMDD dates.")
    try:
        response = httpx.get(
            "https://power.larc.nasa.gov/api/temporal/daily/point",
            params={
                "parameters": "ALLSKY_SFC_SW_DWN", "community": "RE",
                "longitude": lon, "latitude": lat, "start": start, "end": end,
                "format": "JSON", "time-standard": "UTC",
            },
            timeout=25.0,
        )
        response.raise_for_status()
        payload = response.json()
        values = payload["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        valid = [float(v) for v in values.values() if v is not None and float(v) >= 0]
        if not valid:
            raise ValueError("NASA POWER returned no valid irradiation values for this period.")
        annual_ghi = sum(valid)
        mean_daily = annual_ghi / len(valid)
        specific_yield = annual_ghi * performance_ratio
        return {
            "source": "NASA POWER",
            "source_url": "https://power.larc.nasa.gov/docs/services/api/temporal/daily/",
            "parameter": "ALLSKY_SFC_SW_DWN",
            "parameter_description": "All-sky surface shortwave downward irradiation",
            "unit": "kWh/m2/day",
            "latitude": lat, "longitude": lon, "start": start, "end": end,
            "valid_days": len(valid), "mean_daily_ghi_kwh_m2_day": round(mean_daily, 3),
            "period_ghi_kwh_m2": round(annual_ghi, 2),
            "performance_ratio_assumption": performance_ratio,
            "indicative_specific_yield_mwh_per_mw_year": round(specific_yield, 1),
            "status": "resource-screening-estimate-not-bankable-yield",
            "limitations": [
                "NASA POWER is gridded satellite/reanalysis resource data, not an on-site pyranometer measurement.",
                "This simplified estimate applies a stated performance ratio to horizontal irradiation; it is not a PV simulation.",
                "It does not model array tilt, azimuth, shading, temperature losses, clipping, soiling, degradation, downtime or curtailment.",
                "Use site-specific design and independent resource validation for financing and engineering decisions.",
            ],
        }
    except HTTPException:
        raise
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Solar-resource provider unavailable or returned an unusable response.") from exc

@app.post("/api/v1/solar/potential")
def estimate_solar_potential(payload: SolarPotentialRequest):
    capacity = payload.usable_area_m2 * payload.installed_density_w_per_m2 / 1_000_000
    annual_mwh = capacity * payload.specific_yield_mwh_per_mw_year
    response = {
        "usable_area_m2": payload.usable_area_m2,
        "installed_density_w_per_m2": payload.installed_density_w_per_m2,
        "estimated_capacity_mw_dc": round(capacity, 4),
        "specific_yield_mwh_per_mw_year": payload.specific_yield_mwh_per_mw_year,
        "estimated_annual_generation_mwh": round(annual_mwh, 2),
        "status": "planning-estimate-not-metered-generation",
        "notice": "Planning-stage estimate based on user-supplied assumptions. It is not measured generation, grid acceptance or a carbon-credit calculation.",
    }
    if payload.grid_emission_factor_tco2e_per_mwh is not None:
        response["indicative_avoided_emissions_tco2e_per_year"] = round(
            annual_mwh * payload.grid_emission_factor_tco2e_per_mwh, 2
        )
        response["emissions_status"] = "indicative-planning-screen-only-not-mrv"
    return response

@app.post("/api/v1/projects", status_code=201)
def create_project(payload: ProjectCreate):
    if payload.district not in DISTRICTS:
        raise HTTPException(status_code=422, detail="District must be in Telangana.")
    project_id = str(uuid4())
    record = {
        "project_id": project_id, **payload.model_dump(),
        "state": "Telangana", "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "registered-unverified", "mrv_status": "meter-data-pending",
    }
    projects[project_id] = record
    meter_readings[project_id] = []
    log_event("project", project_id, "project-registered", {"data_status": payload.data_status})
    return record

@app.get("/api/v1/projects")
def list_projects():
    return list(projects.values())

@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return {**projects[project_id], "meter_record_count": len(meter_readings.get(project_id, []))}

@app.post("/api/v1/projects/{project_id}/meter-readings")
def add_meter_readings(project_id: str, payload: MeterBatch):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    existing = meter_readings[project_id]
    known = {(r["timestamp"], r["meter_id"], r["reading_type"]) for r in existing}
    accepted, duplicates = [], 0
    for item in payload.readings:
        row = item.model_dump()
        row["timestamp"] = row["timestamp"].isoformat()
        key = (row["timestamp"], row["meter_id"], row["reading_type"])
        if key in known:
            duplicates += 1
            continue
        known.add(key)
        accepted.append(row)
    existing.extend(accepted)
    projects[project_id]["mrv_status"] = "meter-data-uploaded"
    log_event("project", project_id, "meter-data-ingested", {"accepted": len(accepted), "duplicates": duplicates})
    return {"project_id": project_id, "accepted": len(accepted), "duplicates_skipped": duplicates,
            "total_records": len(existing), "status": "uploaded-not-yet-verified"}

@app.post("/api/v1/projects/{project_id}/meter-csv")
async def upload_meter_csv(project_id: str, file: UploadFile = File(...)):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Upload a CSV file.")
    raw = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw))
    required = {"timestamp", "energy_mwh", "meter_id"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(status_code=422, detail="CSV columns required: timestamp,energy_mwh,meter_id; optional: reading_type,source")
    rows = []
    for line, row in enumerate(reader, start=2):
        try:
            rows.append(MeterReading(
                timestamp=datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")),
                energy_mwh=float(row["energy_mwh"]), meter_id=row["meter_id"],
                reading_type=row.get("reading_type") or "generation",
                source=row.get("source") or file.filename,
            ))
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Invalid CSV row {line}: {exc}") from exc
    return add_meter_readings(project_id, MeterBatch(readings=rows))

@app.get("/api/v1/projects/{project_id}/meter-readings")
def get_meter_readings(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    rows = meter_readings.get(project_id, [])
    return {"project_id": project_id, "count": len(rows), "readings": rows}

@app.post("/api/v1/projects/{project_id}/mrv")
def calculate_mrv(project_id: str, payload: MRVRequest):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    rows = meter_readings.get(project_id, [])
    eligible = sum(r["energy_mwh"] for r in rows if r["reading_type"] == payload.eligible_energy_basis)
    baseline = eligible * payload.grid_emission_factor_tco2e_per_mwh
    net = max(0.0, baseline - payload.project_emissions_tco2e - payload.leakage_tco2e)
    result = {
        "project_id": project_id, "methodology_name": payload.methodology_name,
        "eligible_energy_basis": payload.eligible_energy_basis, "eligible_energy_mwh": round(eligible, 6),
        "grid_emission_factor_tco2e_per_mwh": payload.grid_emission_factor_tco2e_per_mwh,
        "factor_source": payload.factor_source, "factor_vintage": payload.factor_vintage,
        "baseline_emissions_tco2e": round(baseline, 6),
        "project_emissions_tco2e": payload.project_emissions_tco2e,
        "leakage_tco2e": payload.leakage_tco2e, "indicative_net_avoided_emissions_tco2e": round(net, 6),
        "status": "indicative-estimate-not-verified",
        "credit_issuance_status": "not-assessed-no-credits-issued",
        "limitations": [
            "This is an indicative calculation, not a methodology-approved credit calculation.",
            "Meter readings are user-uploaded and have not been independently verified.",
            "Additionality, ownership, regulatory surplus, leakage, safeguards and double counting have not been assessed.",
            "A substation association does not prove grid connection or eligible electricity delivery.",
        ],
    }
    projects[project_id]["mrv_status"] = "indicative-estimate-created"
    log_event("project", project_id, "indicative-mrv-calculated", {"factor_source": payload.factor_source, "energy_mwh": round(eligible, 6)})
    return result

@app.get("/api/v1/projects/{project_id}/audit")
def project_audit(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return [e for e in audit_events if e["entity_id"] == project_id]

@app.get("/api/v1/map/layers")
def map_layers():
    return {
        "state": "Telangana",
        "substations": {
            "provider": "TGRAC public ArcGIS service",
            "url": "https://tgrac.telangana.gov.in/arcgis/rest/services/RRR_Folder/RRR/MapServer/8",
            "status": "external-live-layer-not-utility-verified",
        },
        "basemap": "OpenStreetMap / CARTO",
        "notice": "Mapped infrastructure is contextual GIS data; confirm asset identity, voltage, operational status and electrical connection with the utility.",
    }


# Read-only PostGIS spatial endpoints (existing demo/MRV routes remain unchanged).
from backend.spatial import router as spatial_router
app.include_router(spatial_router)
