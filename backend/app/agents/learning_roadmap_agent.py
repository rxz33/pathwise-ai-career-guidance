# app/agents/learning_roadmap_agent.py
from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class LearningRoadmapAgent(BaseAgent):
    async def analyze_learning(self, learning_data: Dict, strengths_and_weaknesses: Dict) -> Dict:
        prompt = f"""
        Analyze user's learning roadmap in relation to strengths and weaknesses.
        Learning data: {learning_data}
        Strengths/Weaknesses: {strengths_and_weaknesses}
        Return JSON summary with: learning_gaps, recommendations, next_steps.
        """
        raw = await self.call_llm_cached("learning_summary", prompt)
        return safe_json_parse(raw, fallback={})
