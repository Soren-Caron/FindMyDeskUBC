import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
import pandas as pd
import json
from datetime import datetime, timezone

from model import train_model, predict_busy_score


def test_train_model(tmp_path, monkeypatch):
    csv = tmp_path / "desk_logs.csv"
    df = pd.DataFrame({
        "desk": ["Lam Circ", "Lam Circ", "Educ Circ"],
        "date_time": [
            "2024-01-01T01:00:00Z",
            "2024-01-01T04:00:00Z",
            "2024-01-01T04:00:00Z",
        ]
    })
    df.to_csv(csv, index=False)

    monkeypatch.setattr("model.DESK_LOGS_PATH", csv)
    monkeypatch.setattr("model.LOOKUP_PATH", tmp_path / "lookup.json")
    monkeypatch.setattr("model.DATA_DIR", tmp_path)

    lookup = train_model()
    assert "per_library" in lookup
    assert "global" in lookup
    assert (tmp_path / "lookup.json").exists()


def test_predict_busy_score(tmp_path, monkeypatch):
    lookup_json = tmp_path / "lookup.json"
    lookup_json.write_text(json.dumps({
        "per_library": {"Koerner": {"0": 0.8}},
        "global": {"0": 0.5}
    }))

    monkeypatch.setattr("model.LOOKUP_PATH", lookup_json)
    monkeypatch.setattr("model.get_feedback_score", lambda *a, **k: 0.6)

    monkeypatch.setattr(
        "model.get_weather",
        lambda ts: {"temp": 10, "precip": 1, "cloud": 50, "wind": 5},
    )

    now = datetime(2024, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
    result = predict_busy_score("Koerner", now.isoformat())

    assert result["model_score"] == 0.8
    assert result["feedback_score"] == 0.6
    assert 0 <= result["busy_score"] <= 1
