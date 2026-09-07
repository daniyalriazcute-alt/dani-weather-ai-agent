import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_location(location: str):
    response = requests.get(
        GEOCODE_URL,
        params={"name": location, "count": 1, "language": "en", "format": "json"},
        timeout=8,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise ValueError("Location not found.")
    item = results[0]
    return {
        "name": item.get("name"),
        "country": item.get("country"),
        "latitude": item["latitude"],
        "longitude": item["longitude"],
        "timezone": item.get("timezone"),
    }

def get_weather(location: str, forecast_days: int = 1):
    if not location or len(location) > 120:
        raise ValueError("Invalid location.")
    if not 1 <= int(forecast_days) <= 7:
        raise ValueError("Forecast days must be between 1 and 7.")

    place = geocode_location(location)
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "daily": ",".join([
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum",
            ]),
            "forecast_days": int(forecast_days),
            "timezone": "auto",
        },
        timeout=8,
    )
    response.raise_for_status()
    data = response.json()

    return {
        "location": place,
        "timezone": data.get("timezone"),
        "daily": data.get("daily", {}),
        "units": data.get("daily_units", {}),
        "source": "Open-Meteo",
    }
