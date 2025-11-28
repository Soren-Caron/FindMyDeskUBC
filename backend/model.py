# backend/model.py

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from weather import get_weather  # must return dict with temp/precip/cloud/wind

# ---------- Paths ----------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DESK_LOGS_PATH = DATA_DIR / "desk_logs.csv"
FEEDBACK_PATH = DATA_DIR / "feedback.csv"   # optional (Supabase export)
LOOKUP_PATH = DATA_DIR / "lookup.json"

# ---------- Libraries & Mapping ----------

TARGET_LIBRARIES = {
    "IKBLC",
    "Koerner",
    "David Lam",
    "Education",
    "Woodward",
    "Law",
    "Asian",
    "Xwi7xwa",
    "Chapman",
}

# Map raw "desk" values (from CSV) -> our library labels
DESK_TO_LIBRARY: Dict[str, str] = {
    # David Lam
    "Lam Circ": "David Lam",
    "Lam Ref": "David Lam",
    "David Lam Circ": "David Lam",
    "David Lam Ref": "David Lam",

    # Education
    "Educ Circ": "Education",
    "Educ Ref": "Education",
    "Education Circ": "Education",
    "Education Ref": "Education",

    # Woodward
    "Woodward Circ": "Woodward",
    "Woodward Ref": "Woodward",

    # Law
    "Law Circ": "Law",
    "Law Ref": "Law",
    "Law Library Circ": "Law",

    # Asian
    "Asian Circ": "Asian",
    "Asian Ref": "Asian",

    # Xwi7xwa
    "Xwi7xwa Circ": "Xwi7xwa",
    "Xwi7xwa Ref": "Xwi7xwa",
    "Xwi7xwa Off Desk": "Xwi7xwa",

    # Chapman / IKBLC region
    "Chapman": "Chapman",
    "Chapman LC": "Chapman",
    "Chapman LC Desk": "Chapman",

    # TODO: if you discover IKBLC desks in the CSV, add them here:
    # "IKB Circ": "IKBLC",
    # "IKBLC Circ": "IKBLC",
}


def normalize_desk_to_library(raw: Any) -> Optional[str]:
    """
    Map a raw 'desk' string from the CSV to one of our TARGET_LIBRARIES.
    Returns None if it can't be mapped.
    """
    if pd.isna(raw):
        return None

    s = str(raw).strip()

    # Direct mapping first
    if s in DESK_TO_LIBRARY:
        return DESK_TO_LIBRARY[s]

    # Fuzzy "contains" mapping, in case the desk label has extra text
    lower = s.lower()
    for key, lib in DESK_TO_LIBRARY.items():
        if key.lower() in lower:
            return lib

    return None


def get_bin_from_hour(hour: int) -> int:
    """
    Convert an hour (0–23) into a 3-hour bin index 0–7.

      0 → [00:00–02:59]
      1 → [03:00–05:59]
      ...
      7 → [21:00–23:59]
    """
    return hour // 3


# ---------- Training ----------

def train_model() -> Dict[str, Any]:
    """
    Train a simple frequency-based model:

      • Read desk_logs.csv
      • Map 'desk' to our library names
      • Filter to TARGET_LIBRARIES
      • Bucket timestamps into 3-hour bins
      • For each library, count observations per bin and normalize:
            count / max_count_for_that_library
      • Also build a global pattern across all libraries

    Returns a lookup dict like:

        {
          "per_library": {
            "Koerner": { "0": 0.12, "1": 0.09, ... },
            "David Lam": { ... },
            ...
          },
          "global": {
            "0": 0.24,
            "1": 0.31,
            ...
          }
        }

    This is also saved as data/lookup.json.
    """
    if not DESK_LOGS_PATH.exists():
        raise FileNotFoundError(f"Desk logs file not found at {DESK_LOGS_PATH}")

    print("📘 Loading desk logs…")
    df = pd.read_csv(DESK_LOGS_PATH, low_memory=False)

    required_cols = {"desk", "date_time"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"desk_logs.csv missing required columns: {required_cols}")

    # Map 'desk' to "library"
    df["library"] = df["desk"].apply(normalize_desk_to_library)

    # Keep only libraries we actually show on the map
    df = df[df["library"].isin(TARGET_LIBRARIES)].copy()

    if df.empty:
        raise ValueError("No matching study spots in the desk logs after mapping.")

    # Parse timestamps; force UTC so we never get tz-mismatch later
    df["dt"] = pd.to_datetime(df["date_time"], errors="coerce", utc=True)
    df = df.dropna(subset=["dt"])

    df["hour"] = df["dt"].dt.hour
    df["bin"] = df["hour"].apply(get_bin_from_hour)  # 0–7

    # ----- Per-library pattern -----
    per_lib_counts = (
        df.groupby(["library", "bin"])
        .size()
        .reset_index(name="count")
    )

    per_library_lookup: Dict[str, Dict[str, float]] = {}

    for lib in per_lib_counts["library"].unique():
        sub = per_lib_counts[per_lib_counts["library"] == lib]
        max_count = sub["count"].max()
        if max_count == 0:
            continue

        per_library_lookup[lib] = {}
        for _, row in sub.iterrows():
            b = int(row["bin"])
            score = row["count"] / max_count
            per_library_lookup[lib][str(b)] = round(float(score), 4)

    # ----- Global pattern (all libraries combined) -----
    global_counts = (
        df.groupby("bin")
        .size()
        .reset_index(name="count")
    )
    max_global = global_counts["count"].max()
    global_lookup: Dict[str, float] = {}

    for _, row in global_counts.iterrows():
        b = int(row["bin"])
        score = row["count"] / max_global if max_global else 0.0
        global_lookup[str(b)] = round(float(score), 4)

    lookup: Dict[str, Any] = {
        "per_library": per_library_lookup,
        "global": global_lookup,
    }

    DATA_DIR.mkdir(exist_ok=True)
    with open(LOOKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(lookup, f, indent=2)

    print("✅ Training complete.")
    print(f"  Libraries modeled: {list(per_library_lookup.keys())}")
    print(f"  Global bins: {len(global_lookup)}")

    return lookup


# ---------- Feedback integration ----------

FEEDBACK_WINDOW_DAYS = 14  # look back this many days for recent feedback


def get_feedback_score(spot: str, now: Optional[datetime] = None) -> Optional[float]:
    """
    Look at feedback.csv and compute an average busy score for this spot
    over the last FEEDBACK_WINDOW_DAYS, normalized into [0,1].

    Expected feedback.csv columns (lowercased after normalization):

      • spot_id       – string matching our "spot" name (e.g. "Koerner")
      • busy_rating   – numeric, 1–10
      • created_at    – optional; if present we time-filter

    If file is missing, malformed, or no valid rows → returns None.
    """
    if not FEEDBACK_PATH.exists():
        return None

    try:
        df = pd.read_csv(FEEDBACK_PATH)
    except Exception:
        return None

    if df.empty:
        return None

    # Normalize column names (lowercase, strip spaces)
    df.columns = [c.strip().lower() for c in df.columns]

    if not {"spot_id", "busy_rating"}.issubset(df.columns):
        return None

    # Parse & time-filter if created_at exists
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
        df = df.dropna(subset=["created_at"])
        if df.empty:
            return None

        # Ensure 'now' is tz-aware UTC to avoid tz-mismatch errors
        if now is None:
            now = datetime.now(timezone.utc)
        else:
            if now.tzinfo is None:
                now = now.replace(tzinfo=timezone.utc)
            else:
                now = now.astimezone(timezone.utc)

        cutoff = now - timedelta(days=FEEDBACK_WINDOW_DAYS)
        df = df[df["created_at"] >= cutoff]
        if df.empty:
            return None

    # Filter by spot/library name (case-insensitive)
    df = df[df["spot_id"].astype(str).str.upper() == spot.upper()]
    if df.empty:
        return None

    # Convert busy_rating to numeric and drop NaN
    df["busy_rating"] = pd.to_numeric(df["busy_rating"], errors="coerce")
    df = df.dropna(subset=["busy_rating"])
    if df.empty:
        return None

    avg = df["busy_rating"].mean()              # 1–10 scale
    score_0_1 = max(0.0, min(1.0, avg / 10.0))  # normalize to 0–1

    return float(round(score_0_1, 4))


# ---------- Lookup load ----------

def load_lookup() -> Dict[str, Any]:
    if not LOOKUP_PATH.exists():
        raise FileNotFoundError("lookup.json not found. Call /train first.")
    with open(LOOKUP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Weather adjustment ----------

def apply_weather_adjustment(
    base_score: float,
    dt: Optional[datetime],
) -> Tuple[float, Dict[str, Any]]:
    """
    Call get_weather() and adjust the base_score based on:
      • precipitation
      • temperature
      • cloud cover
      • wind speed

    Returns (adjusted_score, weather_details_dict).
    """
    # Ensure ISO string in UTC
    if dt is not None:
        if dt.tzinfo is None:
            dt_utc = dt.replace(tzinfo=timezone.utc)
        else:
            dt_utc = dt.astimezone(timezone.utc)
        timestamp_iso = dt_utc.isoformat()
    else:
        dt_utc = None
        timestamp_iso = None

    try:
        weather = get_weather(timestamp_iso)
    except Exception as exc:
        # If weather API fails, just return base score
        return base_score, {
            "error": str(exc),
            "weather_factor": 0.0,
            "before_weather": round(float(base_score), 4),
            "after_weather": round(float(base_score), 4),
        }

    wf = 0.0

    temp = weather.get("temp")
    precip = weather.get("precip")
    cloud = weather.get("cloud")
    wind = weather.get("wind")

    # Simple heuristics – tune these later if you like
    if precip is not None:
        # Light rain → more people study indoors
        if precip > 0.1:
            wf += 0.15
        # Heavy rain → even more indoors
        if precip > 2.0:
            wf += 0.25

    if temp is not None:
        # Hot → fewer indoors
        if temp >= 23:
            wf -= 0.10
        # Cold → more indoors
        elif temp <= 5:
            wf += 0.10

    if cloud is not None:
        # More cloud → slightly more inside
        wf += (cloud / 100.0) * 0.05

    if wind is not None and wind > 20:
        # Strong wind → slightly more inside
        wf += 0.05

    # Clamp the weather factor so it can't break everything
    wf = max(-0.35, min(0.35, wf))

    # Apply and clamp final score into [0.01, 1.0]
    adjusted = base_score + wf
    adjusted = max(0.01, min(1.0, adjusted))

    weather_details = {
        "raw": weather,
        "weather_factor": round(wf, 4),
        "before_weather": round(float(base_score), 4),
        "after_weather": round(float(adjusted), 4),
        "timestamp_utc": dt_utc.isoformat() if dt_utc is not None else None,
    }

    return adjusted, weather_details


# ---------- Main Prediction ----------

def predict_busy_score(spot: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
    """
    Combine:
      1. 3-hour bin pattern from desk logs (per library or global fallback)
      2. Recent feedback (if available via feedback.csv)
      3. Weather adjustment via get_weather()

    Returns a JSON-serializable dict like:

      {
        "spot": "Koerner",
        "timestamp_used": "...",
        "bin": 4,
        "model_score": 0.73,
        "model_source": "per_library",
        "feedback_score": 0.6,
        "blend": "blend_model_0.75_feedback_0.25",
        "score_before_weather": 0.698,
        "weather": { ... },
        "busy_score": 0.82
      }
    """
    lookup = load_lookup()

    # --- Determine the time to use ---
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp)
        except ValueError:
            # If bad timestamp, fall back to "now"
            dt = datetime.utcnow()
    else:
        dt = datetime.utcnow()

    bin_id = get_bin_from_hour(dt.hour)
    bin_key = str(bin_id)

    # --- 1) Model score from desk logs ---
    per_library = lookup.get("per_library", {})
    global_lookup = lookup.get("global", {})

    lib_bins = per_library.get(spot)
    if lib_bins and bin_key in lib_bins:
        model_score = float(lib_bins[bin_key])
        model_source = "per_library"
    else:
        model_score = float(global_lookup.get(bin_key, 0.5))  # fallback mid-busy
        model_source = "global_fallback"

    # --- 2) Feedback score (recent) ---
    feedback_score = get_feedback_score(spot, now=dt)

    if feedback_score is None:
        blended_score = model_score
        blend_info = "no_feedback_model_only"
    else:
        blended_score = 0.75 * model_score + 0.25 * feedback_score
        blend_info = "blend_model_0.75_feedback_0.25"

    blended_score = max(0.0, min(1.0, blended_score))

    # --- 3) Weather adjustment ---
    final_score, weather_details = apply_weather_adjustment(blended_score, dt)

    return {
        "spot": spot,
        "timestamp_used": dt.isoformat(),
        "bin": bin_id,
        "model_score": round(model_score, 4),
        "model_source": model_source,
        "feedback_score": feedback_score,
        "blend": blend_info,
        "score_before_weather": round(blended_score, 4),
        "weather": weather_details,
        "busy_score": round(final_score, 4),
    }
