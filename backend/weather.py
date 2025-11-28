import requests
from datetime import datetime, timezone

# UBC Vancouver lat/lon
UBC_LAT = 49.2606
UBC_LON = -123.2460

def get_weather(timestamp_iso: str):
    """
    Returns weather conditions at the given timestamp.
    Uses Open-Meteo's free historical+forecast API.
    """
    if timestamp_iso is None:
        timestamp_iso = datetime.now(timezone.utc).isoformat()

    # Parse timestamp to date/hour
    dt = datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00"))
    date_str = dt.strftime("%Y-%m-%d")
    hour = dt.hour

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={UBC_LAT}&longitude={UBC_LON}"
        "&hourly=temperature_2m,precipitation,cloud_cover,wind_speed_10m"
        "&forecast_days=16&past_days=16"
    )

    try:
        res = requests.get(url, timeout=5)
        data = res.json()
    except:
        return {"temp": None, "precip": None, "cloud": None, "wind": None}

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])

    # Find closest hour index
    try:
        idx = times.index(f"{date_str}T{hour:02d}:00")
    except ValueError:
        return {"temp": None, "precip": None, "cloud": None, "wind": None}

    return {
        "temp": hourly["temperature_2m"][idx],
        "precip": hourly["precipitation"][idx],
        "cloud": hourly["cloud_cover"][idx],
        "wind": hourly["wind_speed_10m"][idx],
    }
