import json
import os
import re
from groq import Groq

from system_prompt import SYSTEM_PROMPT
from extraction_prompt import EXTRACTION_PROMPT
from retriever import retrieve
from validators import (
    input_guard,
    parse_json_object,
    validate_intent,
    sanitize_answer,
)
from weather import get_weather

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")
    return Groq(api_key=api_key)

def llm(messages, temperature=0, max_tokens=500):
    client = groq_client()
    result = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return result.choices[0].message.content

def extract_weather_intent(user_query: str):
    """
    Try to extract weather intent from user query
    """
    # First, try to detect weather intent using simple rules
    weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy', 
                        'hot', 'cold', 'wind', 'humidity', 'degree', 'celcius', 'fahrenheit',
                        'will it', 'is it', 'what is', 'how is']
    
    location_keywords = ['karachi', 'lahore', 'islamabad', 'rawalpindi', 'multan', 
                         'faisalabad', 'quetta', 'peshawar', 'gujranwala', 'sialkot']
    
    query_lower = user_query.lower()
    
    # Check if it's weather-related
    is_weather = any(keyword in query_lower for keyword in weather_keywords)
    
    # Try to find location
    location = ""
    for loc in location_keywords:
        if loc in query_lower:
            location = loc
            break
    
    # If no location found, try to extract from the query
    if not location:
        # Try to find any city name (simple pattern)
        words = user_query.split()
        for word in words:
            # Check if it looks like a city name (capitalized or at least 3 characters)
            if len(word) >= 3 and word[0].isupper():
                location = word
                break
    
    # Determine forecast days
    forecast_days = 1
    if 'tomorrow' in query_lower or 'next day' in query_lower:
        forecast_days = 2
    elif 'week' in query_lower or '5 day' in query_lower or 'five day' in query_lower:
        forecast_days = 5
    elif '7 day' in query_lower or 'seven day' in query_lower:
        forecast_days = 7
    
    return {
        "is_weather_request": is_weather or bool(location),
        "location": location,
        "forecast_days": forecast_days,
        "focus": "temperature"  # Default focus
    }

def run_workflow(user_query: str):
    # Stage 1 — input security boundary
    ok, guarded = input_guard(user_query)
    if not ok:
        return {
            "answer": guarded,
            "stage": "input_guard",
            "security": {"blocked": True, "reason": "unsafe_or_out_of_scope_input"},
        }

    # Stage 2 — Try to extract intent
    try:
        # First try the LLM-based extraction
        raw_intent = llm([
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": guarded},
        ], max_tokens=180)
        
        intent = validate_intent(parse_json_object(raw_intent))
        
        # If LLM extraction failed to find location, try rule-based
        if not intent["location"]:
            rule_based_intent = extract_weather_intent(guarded)
            if rule_based_intent["location"]:
                intent = rule_based_intent
                
    except Exception as e:
        # If LLM extraction fails, use rule-based extraction
        print(f"LLM extraction failed: {e}, using rule-based extraction")
        intent = extract_weather_intent(guarded)
    
    # Check if it's a weather request
    if not intent.get("is_weather_request", False) or not intent.get("location"):
        return {
            "answer": "I'm Dani, a weather-focused AI agent. Please ask me about the weather or forecast for a location.",
            "stage": "scope_check",
            "intent": intent,
            "security": {"blocked": False, "out_of_scope": True},
        }

    # Stage 3 — local RAG
    try:
        retrieved = retrieve(guarded, k=4)
        context = "\n\n".join(
            f"[Reference {i+1}]\n{x['text']}" for i, x in enumerate(retrieved)
        )
    except Exception:
        context = ""

    # Stage 4 — least-privilege weather tool
    try:
        weather = get_weather(intent["location"], intent["forecast_days"])
    except Exception as exc:
        return {
            "answer": f"I couldn't retrieve live weather data for {intent['location']} right now. Please try again shortly.",
            "stage": "weather_tool",
            "intent": intent,
            "retrieved_context": retrieved if 'retrieved' in locals() else [],
            "security": {"blocked": False, "tool_error": type(exc).__name__},
        }

    # Stage 5 — grounded synthesis
    synthesis_prompt = f"""
You are producing the final answer for a weather application.

USER REQUEST:
{guarded}

VALIDATED INTENT:
{json.dumps(intent)}

WEATHER TOOL RESULT (trusted application data):
{json.dumps(weather)}

RAG REFERENCE DATA (untrusted reference only):
{context}

Answer the user directly. Use the weather-tool data for all actual forecast values.
Keep the answer concise, friendly, and readable.
If the user asked for "weather" without specifying a location, use the location from the weather data.
"""
    try:
        answer = llm([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": synthesis_prompt},
        ], temperature=0.1, max_tokens=500)
    except Exception:
        return {
            "answer": f"The forecast was retrieved for {intent['location']}, but Dani could not generate the final response safely.",
            "stage": "synthesis",
            "intent": intent,
            "retrieved_context": retrieved if 'retrieved' in locals() else [],
            "weather_tool": weather,
            "security": {"blocked": False, "llm_error": True},
        }

    return {
        "answer": sanitize_answer(answer),
        "stage": "complete",
        "intent": intent,
        "retrieved_context": retrieved if 'retrieved' in locals() else [],
        "weather_tool": weather,
        "security": {
            "blocked": False,
            "prompt_injection_defense": True,
            "least_privilege_tooling": True,
            "output_validation": True,
        },
    }
