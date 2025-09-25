# app/agents/socioeconomic_agent.py
from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse

class SocioEconomicAgent(BaseAgent):
    async def generate_summary(self, personal_info: Dict, optional_fields: Dict) -> Dict:
        prompt = f"""
        Analyze socio-economic context for career guidance.
        Include location constraints, financial status, risk capacity.
        Personal info: {personal_info}
        Optional fields: {optional_fields}
        Return JSON only with: location_constraints, financial_analysis, risk_capacity, recommendations.
        """
        raw = await self.call_llm_cached("socioeconomic_summary", prompt)
        return safe_json_parse(raw, fallback={})
