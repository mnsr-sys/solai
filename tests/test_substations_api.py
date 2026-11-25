from fastapi.testclient import TestClient

from backend import main

client = TestClient(main.app)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_substation_endpoint_fetches_all_object_ids_in_batches(monkeypatch):
    calls = []

    def fake_get(url, params, timeout):
        calls.append(params)
        if params.get("returnIdsOnly") == "true":
            return FakeResponse({"objectIds": [1, 2, 3]})
        return FakeResponse({
            "features": [
                {"attributes": {"FID": int(value)}, "geometry": {"x": 78.0, "y": 17.0}}
                for value in params["objectIds"].split(",")
            ]
        })

    monkeypatch.setattr(main.httpx, "get", fake_get)
    response = client.get("/api/v1/map/substations")
    assert response.status_code == 200
    body = response.json()
    assert body["source_record_count"] == 3
    assert body["returned_count"] == 3
    assert body["complete_for_source_layer"] is True
    assert len(body["features"]) == 3
    assert calls[0]["returnIdsOnly"] == "true"
    assert calls[1]["outSR"] == "4326"


def test_substation_endpoint_reports_upstream_failure(monkeypatch):
    def fake_get(url, params, timeout):
        raise main.httpx.TimeoutException("upstream timeout")

    monkeypatch.setattr(main.httpx, "get", fake_get)
    response = client.get("/api/v1/map/substations")
    assert response.status_code == 502
