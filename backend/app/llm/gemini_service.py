# services/gemini_service.py
import os
import asyncio
import logging
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger("gemini_service")
logging.basicConfig(level=logging.INFO)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-pro"  # text model

async def ask_gemini(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    try:
        logger.info("Sending prompt to Gemini API...")

        def sync_call():
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
            )
            return response.text.strip()

        response_text = await asyncio.to_thread(sync_call)
        logger.info("Received response from Gemini API")
        return response_text

    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        raise RuntimeError(f"Gemini API call failed: {str(e)}")
