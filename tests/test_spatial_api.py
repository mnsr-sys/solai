from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_spatial_routes_are_registered():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/spatial/health" in paths
    assert "/api/v1/spatial/layers" in paths
    assert "/api/v1/spatial/nearby" in paths


def test_nearby_rejects_unknown_layer_before_database_access():
    response = client.get(
        "/api/v1/spatial/nearby",
        params={"lat": 17.385, "lon": 78.4867, "layers": "not_a_real_layer"},
    )
    assert response.status_code == 422
    assert "available_layers" in response.json()["detail"]
