from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class LearningRoadmapAgent(BaseAgent):
    async def analyze_learning(self, learning_data: Dict, strengths_and_weaknesses: Dict, user_name: str = "User") -> Dict:
        # Only necessary fields
        selected = {
            k: learning_data.get(k) for k in [
                "toolsTechUsed", "internshipOrProject", "relatedToCareer",
                "studyPlan", "preferredLearning", "openToExplore",
                "currentRole", "yearsOfExperience"
            ]
        }

        # Optimized prompt
        prompt = f"""
        Provide a JSON summary for {user_name}'s learning roadmap:
        Learning: {selected}
        Strengths/Weaknesses: {strengths_and_weaknesses}
        JSON keys: learning_gaps, recommendations, next_steps.
        """

        raw = await self.call_llm_cached("learning_summary", prompt)
        return safe_json_parse(raw, fallback={})
