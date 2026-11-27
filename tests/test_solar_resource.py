from fastapi.testclient import TestClient

from backend import main

client = TestClient(main.app)


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "properties": {
                "parameter": {
                    "ALLSKY_SFC_SW_DWN": {
                        "20250101": 5.0,
                        "20250102": 6.0,
                        "20250103": -999.0,
                    }
                }
            }
        }


def test_solar_resource_uses_nasa_power_and_returns_screening_yield(monkeypatch):
    def fake_get(url, params, timeout):
        assert "power.larc.nasa.gov" in url
        assert params["parameters"] == "ALLSKY_SFC_SW_DWN"
        assert params["latitude"] == 17.36
        return FakeResponse()

    monkeypatch.setattr(main.httpx, "get", fake_get)
    response = client.get(
        "/api/v1/solar/resource",
        params={"lat": 17.36, "lon": 78.47, "start": "20250101", "end": "20250103"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "NASA POWER"
    assert body["valid_days"] == 2
    assert body["period_ghi_kwh_m2"] == 11.0
    assert body["indicative_specific_yield_mwh_per_mw_year"] == 8.6
    assert body["status"] == "resource-screening-estimate-not-bankable-yield"


def test_solar_resource_rejects_bad_date_format():
    response = client.get(
        "/api/v1/solar/resource",
        params={"lat": 17.36, "lon": 78.47, "start": "2025-01-01", "end": "20250103"},
    )
    assert response.status_code == 422
