from app.services.cross_exam_service import analyze_cross_exam_answers

class AgentPipeline:
    def __init__(self, email: str):
        self.email = email
        self.results = {}

    async def run_cross_exam(self, answers: dict):
        cross_exam_result = await analyze_cross_exam_answers(self.email, answers)
        self.results.update(cross_exam_result)
        return cross_exam_result

    async def run_pipeline(self, user_input: dict):
        """
        Dummy pipeline manager – later we’ll connect resume parser, gap analysis, etc.
        For now, only runs cross-exam analysis.
        """
        answers = user_input.get("cross_exam_answers", {})
        await self.run_cross_exam(answers)
        return self.results
