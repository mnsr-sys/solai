from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_score_sites_ranks_higher_score_first():
    payload = {
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
    ranked = response.json()["ranked_sites"]
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
