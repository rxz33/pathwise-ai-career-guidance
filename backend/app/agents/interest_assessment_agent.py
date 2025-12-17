# app/agents/aptitude_interest_agent.py
from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse
from app.schemas.user_data import UserData

class AptitudeInterestAgent(BaseAgent):
    async def analyze_tests(self, tests: Dict, interests: Dict, personal_info: Dict = None) -> Dict:
        prompt = f"""
You are a career psychologist AI.

Your task is to analyze the user's TEST RESULTS and INTERESTS separately,
then reconcile them.

Use these rules:
1. Aptitude shows WHAT the user can realistically do well.
2. RIASEC shows WHERE the user will thrive long-term.
3. Interests show WHAT the user wants, not what is optimal.
4. If tests and interests conflict, highlight the conflict clearly.

User Data:
Personal Info: {personal_info}

Tests:
- Aptitude Test: {tests.get("aptitude")}
- RIASEC Test: {tests.get("riasec")}
- Big Five (if present): {tests.get("bigFive")}

Interests:
{interests}

Return ONLY JSON with:
- dominant_aptitudes
- dominant_riasec_types
- interest_alignment (High / Medium / Low)
- conflicts (if any)
- suggested_domains (ranked)
- recommendations (actionable, test-driven)
"""

        raw = await self.call_llm_cached("aptitude_interest_summary", prompt)
        return safe_json_parse(raw, fallback={})

# prompt = f"""
#         Analyze user's tests and interests to suggest career domains.
#         Personal info: {personal_info}
#         Tests: {tests}
#         Interests: {interests}
#         Return JSON summary only with: suggested_domains, recommendations.
#         """