# # app/config.py

# # Default LLM provider per agent
# AGENT_LLM_MAPPING = {
#     "cross_exam": "gemini",       # fast question generation
#     "resume": "gemini",         # reasoning over text
#     "gap_analysis": "gemini",   # deep analysis
#     "recommender": "openai"     # balanced recommendations
# }
AGENT_LLM_MAPPING = {
    "cross_exam": "gemini_flash",         # MUST be Gemini (deep reasoning)
    "gap_analysis": "gemini",       # MUST be Gemini (multi-layer logic)

    "resume": "groq",               # Groq is PERFECT here (cheap + fast)
    "learning": "groq",             # simple summarization
    "aptitude": "groq",             # basic logic only
    "socio": "groq",                # summarization only
    "optional_fields": "groq",      # small extraction
    "recommender": "openai"         # writing + polish
}

