# services/agentic_orchestrator.py

from typing import Dict, Any
from services.resume_agent import ResumeAgent
from services.cross_exam_agent import CrossExamAgent

class AgenticOrchestrator:
    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.cross_exam_agent = CrossExamAgent()

    def preprocess_input(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        processed_data = user_data.copy()
        if "skills" in processed_data and processed_data["skills"]:
            processed_data["skills"] = list(set(
                [s.strip().lower() for s in processed_data["skills"]]
            ))
        return processed_data

    def run_resume_agent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "resume" not in data or not data["resume"]:
            return {"resume_analysis": "No resume uploaded"}
        return {"resume_analysis": self.resume_agent.analyze_resume(data["resume"])}

    def run_cross_exam_agent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"cross_exam_questions": self.cross_exam_agent.generate_questions(data)}

    def run_roadmap_agent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"roadmap": "Suggested top 3 career paths with roadmap"}

    def orchestrate(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        processed = self.preprocess_input(user_data)
        results = {}
        results.update(self.run_resume_agent(processed))
        results.update(self.run_cross_exam_agent(processed))
        results.update(self.run_roadmap_agent(processed))
        return {"processed_data": processed, "analysis": results}
