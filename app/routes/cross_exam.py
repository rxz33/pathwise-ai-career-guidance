import os
from groq import Groq
from typing import Dict, Any

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class CrossExamAnalyzer:
    def __init__(self, email: str):
        self.email = email

    async def run(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        if not answers:
            return {"summary": "No answers provided"}

        # Build prompt
        prompt = f"""
        You are an AI career counselor. Analyze the following cross-exam answers:
        {answers}

        Return JSON with:
        - strengths
        - weaknesses
        - consistency check (are answers genuine?)
        - summary
        """

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # ⚡ Groq LLM
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        # If model returns text JSON, try parsing
        try:
            import json
            return json.loads(content)
        except:
            return {"summary": content, "raw": answers}
