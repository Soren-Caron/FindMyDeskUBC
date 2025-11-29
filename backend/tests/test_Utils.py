import sys
from pathlib import Path

# Add the backend folder to sys.path
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from datetime import datetime, timezone, timedelta
import pandas as pd

from model import (
    normalize_desk_to_library,
    get_bin_from_hour,
    apply_weather_adjustment,
    get_feedback_score,
)


def test_normalize_exact_match():
    assert normalize_desk_to_library("Lam Circ") == "David Lam"


def test_normalize_fuzzy_match():
    assert normalize_desk_to_library("Lam Circ Desk 12") == "David Lam"


def test_normalize_none_input():
    assert normalize_desk_to_library(None) is None


def test_normalize_unknown():
    assert normalize_desk_to_library("Unknown Desk") is None


def test_get_bin_from_hour():
    assert get_bin_from_hour(0) == 0
    assert get_bin_from_hour(2) == 0
    assert get_bin_from_hour(3) == 1
    assert get_bin_from_hour(23) == 7


def test_apply_weather_no_weather(monkeypatch):
    def fake_weather(ts):
        raise RuntimeError("fail")

    monkeypatch.setattr("model.get_weather", fake_weather)

    adj, details = apply_weather_adjustment(0.5, datetime.now(timezone.utc))
    assert adj == 0.5
    assert "error" in details


def test_apply_weather_rain(monkeypatch):
    def fake_weather(ts):
        return {"temp": 10, "precip": 3.0, "cloud": 50, "wind": 5}

    monkeypatch.setattr("model.get_weather", fake_weather)

    adj, _ = apply_weather_adjustment(0.5, datetime.now(timezone.utc))
    assert adj > 0.5


def test_get_feedback_score(tmp_path, monkeypatch):
    feedback_csv = tmp_path / "feedback.csv"

    df = pd.DataFrame({
        "spot_id": ["Koerner", "Koerner"],
        "busy_rating": [8, 6],
        "created_at": [
            (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
        ]
    })
    df.to_csv(feedback_csv, index=False)

    monkeypatch.setattr("model.FEEDBACK_PATH", feedback_csv)

    score = get_feedback_score("Koerner")
    assert 0 < score <= 1
