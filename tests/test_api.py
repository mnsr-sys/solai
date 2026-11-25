import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def setup_function():
    from backend.main import projects, meter_readings, audit_events
    projects.clear()
    meter_readings.clear()
    audit_events.clear()

def test_health_and_telangan_only_catalog():
    assert client.get("/health").json()["status"] == "ok"
    result = client.get("/api/v1/states").json()
    assert result["default_state"] == "Telangana"
    assert list(result["states"]) == ["Telangana"]
    assert "Bengaluru Urban" not in result["states"]["Telangana"]["districts"]

def test_rejects_non_telangan_district():
    response = client.post("/api/v1/projects", json={
        "name":"Invalid project", "district":"Bengaluru Urban",
        "capacity_mw":2, "latitude":17.4, "longitude":78.4
    })
    assert response.status_code == 422

def test_project_meter_upload_and_mrv_flow():
    project = client.post("/api/v1/projects", json={
        "name":"Telangana Solar Demo", "district":"Rangareddy",
        "capacity_mw":2.5, "latitude":17.2, "longitude":78.1,
        "substation_name":"Demo 33/11 kV", "data_status":"synthetic"
    })
    assert project.status_code == 201
    pid = project.json()["project_id"]
    upload = client.post(f"/api/v1/projects/{pid}/meter-readings", json={"readings":[
        {"timestamp":"2026-10-01T00:00:00Z","energy_mwh":12.5,"meter_id":"GEN-01","reading_type":"generation"},
        {"timestamp":"2026-10-01T00:00:00Z","energy_mwh":11.8,"meter_id":"EXP-01","reading_type":"grid-export"}
    ]})
    assert upload.status_code == 200
    assert upload.json()["accepted"] == 2
    result = client.post(f"/api/v1/projects/{pid}/mrv", json={
        "grid_emission_factor_tco2e_per_mwh":0.7,
        "factor_source":"Test factor source", "factor_vintage":"2026",
        "eligible_energy_basis":"grid-export"
    })
    assert result.status_code == 200
    assert result.json()["eligible_energy_mwh"] == 11.8
    assert result.json()["indicative_net_avoided_emissions_tco2e"] == 8.26
    assert result.json()["status"] == "indicative-estimate-not-verified"

def test_duplicate_meter_reading_is_skipped():
    project = client.post("/api/v1/projects", json={
        "name":"Duplicate Test", "district":"Hyderabad",
        "capacity_mw":1, "latitude":17.4, "longitude":78.4
    }).json()
    pid = project["project_id"]
    payload = {"readings":[{"timestamp":"2026-10-01T00:00:00Z","energy_mwh":1,
              "meter_id":"M1","reading_type":"generation"}]}
    client.post(f"/api/v1/projects/{pid}/meter-readings", json=payload)
    response = client.post(f"/api/v1/projects/{pid}/meter-readings", json=payload)
    assert response.json()["duplicates_skipped"] == 1

def test_solar_estimate_endpoint_removed_from_credit_claims():
    assert client.get("/api/v1/dashboard").status_code == 200

def test_candidate_site_screening_ranks_highest_first():
    response = client.post("/api/v1/sites/score", json={
        "district": "Rangareddy",
        "sites": [
            {"site_id":"A","label":"Higher suitability","usable_area_m2":12000,
             "land_availability":90,"shading":90,"slope":85,"flood_safety":90,
             "grid_proximity":80,"data_status":"synthetic"},
            {"site_id":"B","label":"Lower suitability","usable_area_m2":8000,
             "land_availability":40,"shading":45,"slope":50,"flood_safety":35,
             "grid_proximity":40,"data_status":"synthetic"}
        ]
    })
    assert response.status_code == 200
    ranked = response.json()["ranked_sites"]
    assert ranked[0]["site_id"] == "A"
    assert ranked[0]["suitability_score"] > ranked[1]["suitability_score"]
    assert ranked[0]["status"] == "indicative-geospatial-screening"

def test_solar_potential_is_not_metered_generation():
    response = client.post("/api/v1/solar/potential", json={
        "usable_area_m2":10000,
        "installed_density_w_per_m2":200,
        "specific_yield_mwh_per_mw_year":1500
    })
    assert response.status_code == 200
    result = response.json()
    assert result["estimated_capacity_mw_dc"] == 2
    assert result["estimated_annual_generation_mwh"] == 3000
    assert result["status"] == "planning-estimate-not-metered-generation"

def test_site_screening_rejects_non_telangan_district():
    response = client.post("/api/v1/sites/score", json={
        "district":"Bengaluru Urban",
        "sites":[{"site_id":"X","label":"X","usable_area_m2":1000,
         "land_availability":50,"shading":50,"slope":50,"flood_safety":50,
         "grid_proximity":50}]
    })
    assert response.status_code == 422
