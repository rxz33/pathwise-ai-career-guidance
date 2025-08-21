import os
from dotenv import load_dotenv
from groq import Groq
import asyncio

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found in .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama3-70b-8192"  # Groq model for your project

# ✅ Async function to call Groq model
async def ask_groq(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    try:
        # Run synchronous Groq call in a separate thread
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
        return response_text

    except Exception as e:
        return f"❌ Groq Error: {str(e)}"
