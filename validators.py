import json
import re

MAX_INPUT_CHARS = 1000
MAX_LOCATION_CHARS = 120
MAX_RAG_CHUNKS = 4

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous",
    r"disregard\s+(all\s+)?instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+prompt",
    r"developer\s+message",
    r"tool\s+schema",
    r"api\s*key",
    r"secret",
    r"jailbreak",
]

def input_guard(text: str):
    text = (text or "").strip()
    if not text:
        return False, "Please enter a weather question."
    if len(text) > MAX_INPUT_CHARS:
        return False, "Your request is too long. Please keep it under 1000 characters."
    lowered = text.lower()
    if any(re.search(p, lowered) for p in INJECTION_PATTERNS):
        return False, "I can help with weather and forecasts, but I can't provide hidden prompts, secrets, or internal instructions."
    return True, text

def parse_json_object(content: str):
    content = content.strip()
    # Accept fenced JSON only as a convenience, then validate the resulting object.
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    data = json.loads(content)
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object.")
    return data

def validate_intent(data: dict):
    allowed = {"is_weather_request", "location", "forecast_days", "focus"}
    if set(data.keys()) != allowed:
        raise ValueError("Unexpected intent fields.")
    if not isinstance(data["is_weather_request"], bool):
        raise ValueError("Invalid weather-request flag.")
    location = str(data["location"]).strip()
    if len(location) > MAX_LOCATION_CHARS:
        raise ValueError("Location is too long.")
    days = int(data["forecast_days"])
    if not 1 <= days <= 7:
        raise ValueError("Forecast range must be 1-7 days.")
    if data["focus"] not in {"temperature", "precipitation"}:
        raise ValueError("Invalid forecast focus.")
    return {
        "is_weather_request": data["is_weather_request"],
        "location": location,
        "forecast_days": days,
        "focus": data["focus"],
    }

def sanitize_answer(text: str):
    # UI-safe normalization; Streamlit markdown is used intentionally.
    text = str(text).strip()
    if len(text) > 5000:
        text = text[:5000] + "\n\n[Response truncated for safety.]"
    return text
