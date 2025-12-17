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
You are a senior human career counselor AI.

Your task is NOT to be generic.
Your task is to DIFFERENTIATE this user from others with similar skills.

First, internally identify:
- Conflicting signals across data (skills vs aptitude, interests vs reality, ambition vs constraints)
- Overused strengths
- Hidden risks

Then generate a JSON career guidance report with the following rules:

================ REQUIRED OUTPUT =================

1. friendly_summary
- 5–6 lines
- Mention ONE uncomfortable truth gently
- Mention ONE hidden advantage
- Mention ONE practical limitation (finance, location, personality, or learning speed)

2. top_careers (EXACTLY 3)
Each career must include:
- name
- merits (why it fits THIS user specifically)
- demerits (why it may NOT fit this user)
- trends (market trends RELEVANT to this user’s background & constraints)

RULES FOR CAREERS:
• Only 1 career can be a “safe/common” choice
• At least 1 career must be NON-OBVIOUS
• At least 1 career must be HIGH-RISK / HIGH-EFFORT
• If two careers are similar, downgrade one

3. strengths
- Only strengths that are ACTUALLY proven by data

4. weaknesses
- Include at least 1 internal weakness (habits, confidence, communication, indecision)

5. skill_gaps
- Gaps that BLOCK progress (not generic learning suggestions)

6. suggestions
- Actions that REDUCE risk or CONFIRM fit

7. next_steps
- Concrete 30–60–90 day actions

================ USER DATA =================
personal_info={personal_info}
optional_fields={optional_fields}
socio_summary={socio_summary}
resume_summary={resume_summary}
learning_summary={learning_summary}
aptitude_summary={aptitude_summary}
cross_summary={cross_summary}

================ STRICT RULES =================
- Do NOT repeat standard career lists blindly
- Do NOT recommend all tech roles
- Do NOT assume high confidence or clarity
- Every section must feel SPECIFIC to THIS person
- Return ONLY valid JSON
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
