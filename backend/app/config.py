# app/config.py

# Default LLM provider per agent
AGENT_LLM_MAPPING = {
    "cross_exam": "gemini",       # fast question generation
    "resume": "gemini",         # reasoning over text
    "gap_analysis": "gemini",   # deep analysis
    "recommender": "openai"     # balanced recommendations
}
