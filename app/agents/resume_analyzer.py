from typing import Dict
from app.services.llm_service import call_llm
from app.services import mongo_service
import json

class ResumeAnalyzerAgent:
    """
    AI agent to extract structured information from a user's resume
    and store it in MongoDB.
    """

    def __init__(self, llm_provider: str = "gemini"):
        self.llm_provider = llm_provider

    async def analyze_resume(self, email: str, user_data: Dict, resume_text: str) -> Dict:
        """
        Input: user_data, email, and resume text
        Output: structured JSON according to ResumeData schema
        and store it in MongoDB.
        """
        prompt = f"""
        You are an expert career counselor AI.
        Analyze this resume text and extract structured JSON following this schema:

        {{
          "extractedText": "string",
          "skills": ["list of skills"],
          "projects": ["list of projects"],
          "certifications": ["list of certifications"],
          "hasExperience": "Yes/No"
        }}

        Compare with user profile: {user_data}
        Return valid JSON only.
        Resume Text:
        {resume_text}
        """

        response = await call_llm(self.llm_provider, prompt)

        try:
            structured_data = json.loads(response)
        except json.JSONDecodeError:
            cleaned = response.strip("` \n")
            structured_data = json.loads(cleaned)

        # Store structured resume in MongoDB
        await mongo_service.update_user_by_email(email, {"resumeData": structured_data})

        return structured_data
