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
        JSON summary for {user_name}:
        Location: {location}, Financial: {financial_status}
        Personal info: {personal_info}
        Optional: {selected_optional}
        Include keys: location_constraints, financial_analysis, risk_capacity, recommendations.
        """

        raw = await self.call_llm_cached("socioeconomic_summary", prompt)
        return safe_json_parse(raw, fallback={})
