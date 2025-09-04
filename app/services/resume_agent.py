# services/resume_agent.py

from typing import Dict, Any, List
import re

class ResumeAgent:
    """
    Extracts skills, projects, experience summary, and certifications
    from resume text content.
    """

    def __init__(self):
        # Placeholder skill keywords list (expand later)
        self.skill_keywords = [
            "python", "java", "c++", "react", "fastapi",
            "machine learning", "deep learning", "sql", "javascript"
        ]

    def extract_skills(self, text: str) -> List[str]:
        """
        Basic keyword matching for skills.
        Later: replace with LLM-based extraction.
        """
        skills = []
        for kw in self.skill_keywords:
            if re.search(rf"\b{kw}\b", text, re.IGNORECASE):
                skills.append(kw)
        return list(set(skills))

    def extract_projects(self, text: str) -> List[str]:
        """
        Finds sections that look like 'Projects' with bullet points.
        """
        projects = re.findall(r"(?i)(?:project[s]?:)(.*?)(?:\n\n|\Z)", text, re.DOTALL)
        return [p.strip() for p in projects] if projects else []

    def extract_experience_summary(self, text: str) -> str:
        """
        Extracts short experience summary based on 'Experience' keyword.
        """
        match = re.search(r"(?i)experience[:\s](.*?)(?:\n\n|\Z)", text, re.DOTALL)
        return match.group(1).strip() if match else "Not available"

    def extract_certifications(self, text: str) -> List[str]:
        """
        Looks for certifications mentioned under 'Certifications' section.
        """
        certs = re.findall(r"(?i)certifications?:\s*(.*?)(?:\n\n|\Z)", text, re.DOTALL)
        return [c.strip() for c in certs] if certs else []

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Main function that orchestrates resume parsing.
        """
        return {
            "skills": self.extract_skills(resume_text),
            "projects": self.extract_projects(resume_text),
            "experience_summary": self.extract_experience_summary(resume_text),
            "certifications": self.extract_certifications(resume_text),
            "raw_text": resume_text  # for debugging/reference
        }
