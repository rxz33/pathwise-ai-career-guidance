# app/services/resume_parser_service.py
import io
from PyPDF2 import PdfReader
import docx
import re

# Keywords for basic parsing
SKILLS_KEYWORDS = {"python", "java", "react", "sql", "javascript", "c++", "node", "django", "flask"}
CERT_KEYWORDS = {"certified", "certificate", "course", "diploma", "license"}
PROJECT_KEYWORDS = {"project", "assignment", "research", "thesis"}
EDU_KEYWORDS = {"bachelor", "master", "mba", "degree", "university", "college"}

def parse_resume(file_content: bytes, content_type: str) -> dict:
    text = ""

    # ✅ Extract text
    if content_type == "application/pdf":
        reader = PdfReader(io.BytesIO(file_content))
        text = " ".join([page.extract_text() or "" for page in reader.pages])
    elif content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                          "application/msword"]:
        doc = docx.Document(io.BytesIO(file_content))
        text = " ".join([para.text for para in doc.paragraphs])
    else:
        text = file_content.decode("utf-8", errors="ignore")

    text_lower = text.lower()

    # ✅ Extract Skills
    skills = [word for word in SKILLS_KEYWORDS if word in text_lower]

    # ✅ Extract Certifications
    certifications = []
    for line in text.splitlines():
        if any(cert in line.lower() for cert in CERT_KEYWORDS):
            certifications.append(line.strip())

    # ✅ Extract Projects
    projects = []
    for line in text.splitlines():
        if any(proj in line.lower() for proj in PROJECT_KEYWORDS):
            projects.append(line.strip())

    # ✅ Extract Education
    education = []
    for line in text.splitlines():
        if any(edu in line.lower() for edu in EDU_KEYWORDS):
            education.append(line.strip())

    # ✅ Extract Experience Summary (simple heuristic)
    experience = "Yes" if "experience" in text_lower or "worked at" in text_lower else "No"

    return {
        "extracted_text": text[:5000],  # store more text for Agentic AI
        "skills": skills,
        "has_experience": experience,
        "certifications": certifications,
        "projects": projects,
        "education": education
    }
