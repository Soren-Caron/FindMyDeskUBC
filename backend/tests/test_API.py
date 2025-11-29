import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "backend running"


def test_predict_missing_lookup(monkeypatch):
    monkeypatch.setattr("model.LOOKUP_PATH", "does_not_exist.json")

    r = client.get("/predict?spot=Koerner")
    assert r.status_code == 500


def test_predict_success(monkeypatch):
    fake_lookup = {
        "per_library": {"Koerner": {"0": 0.7}},
        "global": {"0": 0.5},
    }

    monkeypatch.setattr("model.load_lookup", lambda: fake_lookup)
    monkeypatch.setattr("model.get_feedback_score", lambda *a, **k: 0.8)
    monkeypatch.setattr(
        "model.get_weather",
        lambda *a, **k: {"temp": 10, "precip": 0, "cloud": 0, "wind": 0},
    )

    r = client.get("/predict?spot=Koerner&timestamp=2024-01-01T01:00:00")
    assert r.status_code == 200
    data = r.json()
    assert data["spot"] == "Koerner"
    assert 0 <= data["busy_score"] <= 1
