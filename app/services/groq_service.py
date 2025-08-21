import os
from dotenv import load_dotenv
from groq import Groq
import asyncio
import logging

# Setup logging
logger = logging.getLogger("groq_service")
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found in .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama3-70b-8192"

async def ask_groq(prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
    try:
        logger.info("Sending prompt to Groq API...")

        def sync_call():
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful AI career counselor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()

        response_text = await asyncio.to_thread(sync_call)
        logger.info("Received response from Groq API")
        return response_text

    except Exception as e:
        logger.error(f"Groq API call failed: {e}")
        # Raise exception instead of returning ❌ string
        raise RuntimeError(f"Groq API call failed: {str(e)}")
