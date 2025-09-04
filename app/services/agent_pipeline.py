from typing import Dict, Any

# Import agents
from app.agents.cross_exam_analyzer import CrossExamAnalyzer
from app.agents.resume_analyzer import ResumeAnalyzer
from app.agents.gap_analyzer import GapAnalyzer
from app.agents.recommender import RecommenderAgent
from app.config import AGENT_LLM_MAPPING


class AgentPipeline:
    """
    Orchestrates execution of multiple agents in sequence.
    Connects resume, tests, cross-exam, gap analysis, and recommendations.
    """

    def __init__(self, email: str):
        self.email = email

    async def run_pipeline(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        results = {}

        # ----------------- 1. Cross-Exam Analyzer -----------------
        cross_exam = CrossExamAnalyzer(self.email, provider=AGENT_LLM_MAPPING["cross_exam"])
        results["cross_exam"] = await cross_exam.run(payload.get("cross_exam_answers", {}))

        # ----------------- 2. Resume Analyzer -----------------
        resume_agent = ResumeAnalyzer(self.email, provider=AGENT_LLM_MAPPING["resume"])
        results["resume"] = await resume_agent.run(payload.get("resume_text", ""))

        # ----------------- 3. Gap Analyzer -----------------
        gap_agent = GapAnalyzer(self.email, provider=AGENT_LLM_MAPPING["gap_analysis"])
        results["career_gaps"] = await gap_agent.run(results)

        # ----------------- 4. Recommendation Agent -----------------
        recommender = RecommenderAgent(self.email, provider=AGENT_LLM_MAPPING["recommender"])
        results["recommendations"] = await recommender.run(results)

        # ----------------- Final Centralized Result -----------------
        return results
