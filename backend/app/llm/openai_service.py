# services/openai_service.py
import os
import asyncio
import logging
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger("openai_service")
logging.basicConfig(level=logging.INFO)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL_NAME = "gpt-4o-mini"  # fast + cheap, you can swap to "gpt-4o"

async def ask_openai(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    try:
        logger.info("Sending prompt to OpenAI API...")

        def sync_call():
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful AI career counselor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()

        response_text = await asyncio.to_thread(sync_call)
        logger.info("Received response from OpenAI API")
        return response_text

    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        raise RuntimeError(f"OpenAI API call failed: {str(e)}")
