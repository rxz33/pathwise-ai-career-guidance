# app/services/resume_parser.py
import io
import re
from typing import Dict, Any

import pdfplumber
import docx


def parse_resume(file_content: bytes, content_type: str) -> Dict[str, Any]:
    text = ""

    # ------------------ Extract text ------------------
    if content_type == "application/pdf":
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif content_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        doc = docx.Document(io.BytesIO(file_content))
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError(f"Unsupported file type: {content_type}")

    text = text.strip()

    # ------------------ Skills extraction (very basic) ------------------
    predefined_skills = [
        "Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript", "React",
        "Node.js", "Django", "Flask", "Machine Learning", "Deep Learning",
        "Data Analysis", "AWS", "Docker", "Kubernetes"
    ]
    skills = [s for s in predefined_skills if re.search(rf"\b{s}\b", text, re.IGNORECASE)]

    # ------------------ Projects extraction ------------------
    projects = []
    if "project" in text.lower():
        project_lines = [
            line.strip()
            for line in text.split("\n")
            if re.search(r"(project|developed|built)", line, re.IGNORECASE)
        ]
        projects.extend(project_lines[:5])  # limit to 5

    # ------------------ Certifications extraction ------------------
    certifications = []
    if "certification" in text.lower() or "certificate" in text.lower():
        cert_lines = [
            line.strip()
            for line in text.split("\n")
            if re.search(r"(certification|certificate)", line, re.IGNORECASE)
        ]
        certifications.extend(cert_lines[:5])  # limit to 5

    # ------------------ Work experience check ------------------
    has_experience = "Yes" if "experience" in text.lower() else "No"

    # ------------------ Final result ------------------
    return {
        "extractedText": text,
        "skills": skills,
        "projects": projects,
        "certifications": certifications,
        "hasExperience": has_experience,
    }
