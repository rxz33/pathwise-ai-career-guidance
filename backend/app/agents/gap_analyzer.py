from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class GapAnalyzerAgent(BaseAgent):
    async def generate_final_report(
        self,
        socio_summary: Dict,
        resume_summary: Dict,
        learning_summary: Dict,
        aptitude_summary: Dict,
        cross_summary: Dict,
        personal_info: Dict,
        optional_fields: Dict
    ) -> Dict:

        # Updated prompt with clear market trends instruction
        prompt = f"""
        You are a professional career counselor AI. Generate a JSON career guidance report.

        Required keys:
        1. friendly_summary: A warm, concise, human-readable paragraph summarizing the user's career potential,
           highlighting strengths, areas to improve, and motivational tips. Make it encouraging and personalized.
        2. top_careers: 3 recommended careers for the user, each with:
           - name
           - merits (3-5)
           - demerits (3-5)
           - current market trends (brief, 2-3 key points on demand, growth, opportunities)
        3. strengths
        4. weaknesses
        5. skill_gaps
        6. suggestions
        7. next_steps

        Use user's data:
        personal_info={personal_info},
        optional_fields={optional_fields},
        socio_summary={socio_summary},
        resume_summary={resume_summary},
        learning_summary={learning_summary},
        aptitude_summary={aptitude_summary},
        cross_summary={cross_summary}

        Return JSON only. Ensure no field is empty. Keep top careers concise, and make friendly_summary motivating.
        """

        raw = await self.call_llm_cached("final_gap_report", prompt)
        result = safe_json_parse(raw, fallback={})

        # Normalize lists to ensure consistency
        for key in ["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"]:
            val = result.get(key)
            if not val:
                result[key] = ["No data available"]
            elif isinstance(val, dict):
                result[key] = [str(v) if v else "No data available" for v in val.values()]
            elif isinstance(val, list):
                result[key] = [str(v) if v else "No data available" for v in val]
            else:
                result[key] = [str(val)]

        # Ensure top_careers exist and each field is filled
        if "top_careers" not in result or not result["top_careers"]:
            result["top_careers"] = [
                {"name": "Career 1", "merits": [], "demerits": [], "trends": []},
                {"name": "Career 2", "merits": [], "demerits": [], "trends": []},
                {"name": "Career 3", "merits": [], "demerits": [], "trends": []},
            ]

        for career in result["top_careers"]:
            career["name"] = career.get("name") or "Unknown Career"
            career["merits"] = career.get("merits") or ["No merits info available"]
            career["demerits"] = career.get("demerits") or ["No demerits info available"]
            career["trends"] = career.get("trends") or ["No market trends info available"]

        # Ensure friendly summary exists
        result["friendly_summary"] = str(result.get(
            "friendly_summary",
            "Here is your friendly career summary based on your profile."
        ))

        return result
