from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class SocioEconomicAgent(BaseAgent):
    async def generate_summary(self, personal_info: Dict, optional_fields: Dict) -> Dict:
        selected_optional = {k: optional_fields.get(k) for k in [
            "favoriteSubjects", "activitiesThatMakeYouLoseTime",
            "onlineContent", "preferredRole", "preferredCompany", "jobPriorities"
        ]}

        user_name = personal_info.get("name", "User")
        location = personal_info.get("location", "Unknown")
        financial_status = personal_info.get("financialStatus", "Not specified")

        # Optimized prompt
        prompt = f"""
You are a practical career counselor AI.

Your task is to analyze the user's socio-economic background and determine
REAL-WORLD CONSTRAINTS on career choices.

User Details:
Name: {user_name}
Location: {location}
Financial Status: {financial_status}

Personal Info:
{personal_info}

Preferences:
{selected_optional}

Analyze and return ONLY JSON with the following keys:

1. location_constraints
- Whether opportunities are limited locally
- Whether relocation or remote work is required
- Any geographic disadvantages or advantages

2. financial_analysis
- What types of careers are financially feasible RIGHT NOW
- What paths are delayed due to cost
- Whether unpaid internships, certifications, or long prep phases are risky

3. risk_capacity
- One of: Low / Medium / High
- Justify based on finances + support system

4. allowed_career_types
- Career types that are realistically viable in the next 1–2 years

5. restricted_career_types
- Career types that are NOT advisable currently

6. recommendations
- Practical advice to reduce constraints (relocation plan, remote strategy, income-first path)

STRICT RULES:
- Be realistic, not motivational
- Do NOT assume ideal conditions
- Explicitly state limitations
- Avoid generic advice
- Return JSON only
"""


        raw = await self.call_llm_cached("socioeconomic_summary", prompt)
        return safe_json_parse(raw, fallback={})

# prompt = f"""
#         JSON summary for {user_name}:
#         Location: {location}, Financial: {financial_status}
#         Personal info: {personal_info}
#         Optional: {selected_optional}
#         Include keys: location_constraints, financial_analysis, risk_capacity, recommendations.
#         """