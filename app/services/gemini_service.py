import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create Gemini model
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ Make Gemini call async using asyncio.to_thread (runs sync function in a thread)
async def ask_gemini(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    try:
        def sync_call():
            return gemini_model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
            ).text.strip()
        
        response_text = await asyncio.to_thread(sync_call)
        return response_text
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
