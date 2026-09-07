import json
import re

MAX_INPUT_CHARS = 1000
MAX_LOCATION_CHARS = 120
MAX_RAG_CHUNKS = 4

# Only block clearly malicious patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous",
    r"disregard\s+(all\s+)?instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+prompt",
    r"developer\s+message",
    r"tool\s+schema",
    r"api\s*key\s*=\s*['\"]?\w+['\"]?",  # Only block if it looks like an actual key
    r"secret\s*=\s*['\"]?\w+['\"]?",      # Only block if it looks like a secret
    r"jailbreak",
    r"rm\s+-rf",  # Dangerous commands
    r"DROP\s+TABLE",  # SQL injection
]

def input_guard(text: str):
    """
    Validate user input. Returns (is_valid, cleaned_or_error_message)
    """
    text = (text or "").strip()
    
    # Check if empty
    if not text:
        return False, "Please enter a weather question."
    
    # Check length
    if len(text) > MAX_INPUT_CHARS:
        return False, "Your request is too long. Please keep it under 1000 characters."
    
    # Check for malicious patterns (only block real threats)
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered, re.IGNORECASE):
            # Only block if it's clearly malicious, not just mentioning the word
            if "api key" in lowered and "=" not in lowered:
                continue  # Just mentioning API key without providing one is fine
            if "secret" in lowered and "=" not in lowered:
                continue  # Just mentioning secret without providing one is fine
            return False, "I can help with weather and forecasts, but I can't process commands or requests for sensitive information."
    
    # Check if it's a weather-related question or a simple greeting
    weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy', 
                        'hot', 'cold', 'wind', 'humidity', 'karachi', 'lahore', 'islamabad',
                        'city', 'today', 'tomorrow', 'week', 'degree', 'celcius', 'fahrenheit',
                        'what', 'how', 'will', 'does', 'is', 'are', 'was']
    
    # Allow any query that's at least 2 characters and not obviously malicious
    # This will allow "Hi", "Karachi", etc.
    if len(text) >= 2:
        return True, text
    
    return False, "Please ask a weather-related question."

def parse_json_object(content: str):
    """
    Parse JSON from LLM response
    """
    content = content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON from the text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            # Return a default structure
            return {
                "is_weather_request": False,
                "location": "",
                "forecast_days": 1,
                "focus": "temperature"
            }
    
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object.")
    return data

def validate_intent(data: dict):
    """
    Validate and normalize intent data from LLM
    """
    # Check required fields with defaults
    required_fields = ["is_weather_request", "location", "forecast_days", "focus"]
    
    # Ensure all fields exist
    for field in required_fields:
        if field not in data:
            data[field] = None
    
    # Validate is_weather_request
    if not isinstance(data["is_weather_request"], bool):
        data["is_weather_request"] = False
    
    # Validate location
    location = str(data["location"]).strip() if data["location"] else ""
    if len(location) > MAX_LOCATION_CHARS:
        location = location[:MAX_LOCATION_CHARS]
    
    # Validate forecast_days
    try:
        days = int(data["forecast_days"])
        if days < 1:
            days = 1
        elif days > 7:
            days = 7
    except (ValueError, TypeError):
        days = 1
    
    # Validate focus
    focus = data["focus"] if data["focus"] in ["temperature", "precipitation"] else "temperature"
    
    return {
        "is_weather_request": data["is_weather_request"],
        "location": location,
        "forecast_days": days,
        "focus": focus,
    }

def sanitize_answer(text: str):
    """
    Clean and normalize the final answer
    """
    text = str(text).strip()
    
    # Remove any potential sensitive information
    text = re.sub(r'API[_\s]*KEY[:\s]*[A-Za-z0-9_\-]+', '[REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'secret[_\s]*KEY[:\s]*[A-Za-z0-9_\-]+', '[REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'password[:\s]*[A-Za-z0-9_\-]+', '[REDACTED]', text, flags=re.IGNORECASE)
    
    # Remove system prompt attempts
    system_patterns = [
        r'system\s*prompt[:\s]*.*?(?=\n|$)',
        r'instructions?[:\s]*.*?(?=\n|$)',
        r'policy[:\s]*.*?(?=\n|$)',
    ]
    for pattern in system_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Truncate if too long
    if len(text) > 5000:
        text = text[:5000] + "\n\n[Response truncated for safety.]"
    
    return text
