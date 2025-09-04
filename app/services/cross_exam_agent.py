# services/cross_exam_agent.py

from typing import Dict, List
import random

class CrossExamAgent:
    """
    Generates personalized cross-exam questions to validate user inputs.
    """

    def generate_questions(self, user_data: Dict) -> List[str]:
        questions = []

        # Pull some context
        name = user_data.get("fullName", "the candidate")
        field = user_data.get("fieldOfStudy", "")
        role = user_data.get("preferredRole", "")
        strengths = user_data.get("strengths", "")
        struggle = user_data.get("struggleWith", "")
        resume_skills = user_data.get("resume_analysis", {}).get("skills", [])

        # Personalized questions
        if field:
            questions.append(f"Why did you choose to study {field}, and do you see yourself building a career in this field?")
        if role:
            questions.append(f"You mentioned interest in {role}. What excites you most about this role?")
        if strengths:
            questions.append(f"You listed {strengths} as a strength. Can you share a real example where you used this effectively?")
        if struggle:
            questions.append(f"You mentioned struggling with {struggle}. What steps are you taking to improve?")
        if resume_skills:
            skill = random.choice(resume_skills)
            questions.append(f"Your resume shows {skill} as a skill. Can you explain how you applied it in a project or internship?")

        # Add a generic consistency check
        questions.append(f"Looking at your aspirations and current skills, where do you feel the biggest gap exists?")

        return questions[:6]  # return up to 6
