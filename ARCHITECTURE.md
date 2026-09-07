# Dani Multi-stage AI Workflow

1. INPUT GUARD
   - Length limit
   - Basic prompt-injection screening
   - Weather-agent scope

2. INTENT EXTRACTION
   - Groq structured JSON extraction
   - Strict fields
   - Location length and forecast-day validation

3. RAG
   - TF-IDF retrieval over a reviewed local corpus
   - Maximum 4 chunks
   - Retrieved content is data, never instructions

4. WEATHER TOOL
   - Geocode location
   - Query Open-Meteo forecast
   - 1–7 day maximum
   - No arbitrary URLs or tool selection from the LLM

5. GROUNDED SYNTHESIS
   - System prompt establishes trust boundaries
   - Tool result is authoritative for forecast values
   - RAG is contextual only

6. OUTPUT SAFETY
   - Response length limit
   - No secrets/system prompt/tool schema disclosure
   - Safe error messages

This intentionally uses a deterministic Python orchestrator rather than allowing the LLM to freely select arbitrary tools.
