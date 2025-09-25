# app/agents/resume_analyzer_agent.py
from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class ResumeAnalyzerAgent(BaseAgent):
    async def analyze_resume(self, resume_text: str, strengths_and_weaknesses: Dict, preferred_role: str = "") -> Dict:
        prompt = f"""
        Extract skills, projects, and gaps from the resume.
        Compare with claimed strengths/weaknesses: {strengths_and_weaknesses}.
        Consider preferred role: {preferred_role}
        Resume: {resume_text[:500]}...
        Return JSON summary with: skills, projects, gaps.
        """
        raw = await self.call_llm_cached("resume_summary", prompt)
        return safe_json_parse(raw, fallback={})
