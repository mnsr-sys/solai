from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_state_catalog_prioritizes_telangan_and_includes_karnataka():
    response = client.get("/api/v1/states")
    assert response.status_code == 200
    result = response.json()
    assert result["default_state"] == "Telangana"
    assert result["priority_order"] == ["Telangana", "Karnataka"]
    assert "Hyderabad" in result["states"]["Telangana"]["districts"]
    assert "Bengaluru Urban" in result["states"]["Karnataka"]["districts"]


def test_project_accepts_karnataka_demo_district():
    response = client.post("/api/v1/projects", json={
        "name": "Karnataka sample assessment",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "data_status": "synthetic"
    })
    assert response.status_code == 201
    assert response.json()["state"] == "Karnataka"


def test_project_rejects_unknown_district_for_selected_state():
    response = client.post("/api/v1/projects", json={
        "name": "Invalid district test",
        "state": "Telangana",
        "district": "Bengaluru Urban",
        "data_status": "synthetic"
    })
    assert response.status_code == 422


def test_score_sites_ranks_higher_score_first_and_returns_geography():
    payload = {
        "state": "Telangana",
        "district": "Hyderabad",
        "sites": [
            {
                "site_id": "A",
                "label": "Sample A",
                "usable_area_m2": 10000,
                "land_availability": 90,
                "shading": 90,
                "slope": 90,
                "flood_safety": 90,
                "grid_proximity": 90,
                "data_status": "synthetic"
            },
            {
                "site_id": "B",
                "label": "Sample B",
                "usable_area_m2": 5000,
                "land_availability": 30,
                "shading": 40,
                "slope": 50,
                "flood_safety": 40,
                "grid_proximity": 30,
                "data_status": "synthetic"
            }
        ]
    }
    response = client.post("/api/v1/sites/score", json=payload)
    assert response.status_code == 200
    result = response.json()
    ranked = result["ranked_sites"]
    assert result["state"] == "Telangana"
    assert result["district"] == "Hyderabad"
    assert ranked[0]["site_id"] == "A"
    assert ranked[0]["suitability_score"] > ranked[1]["suitability_score"]


def test_solar_estimate():
    response = client.post("/api/v1/solar/estimate", json={
        "usable_area_m2": 10000,
        "installed_density_w_per_m2": 200,
        "specific_yield_mwh_per_mw_year": 1500,
        "grid_emission_factor_tco2e_per_mwh": 0.7
    })
    assert response.status_code == 200
    result = response.json()
    assert result["estimated_capacity_mw_dc"] == 2.0
    assert result["estimated_annual_generation_mwh"] == 3000
    assert result["estimated_avoided_emissions_tco2e_per_year"] == 2100
