# app/services/resume_parser_service.py
import io
from PyPDF2 import PdfReader
import docx

def parse_resume(file_content: bytes, content_type: str) -> dict:
    """
    Extracts text and structured info from resume file.
    """
    text = ""

    # ✅ Extract text depending on file type
    if content_type == "application/pdf":
        reader = PdfReader(io.BytesIO(file_content))
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        doc = docx.Document(io.BytesIO(file_content))
        text = " ".join([para.text for para in doc.paragraphs])
    else:
        text = file_content.decode("utf-8", errors="ignore")

    # ✅ Simple parsing logic (later, Agentic AI will refine this)
    skills = [word for word in text.split() if word.lower() in {"python", "java", "react", "sql"}]
    experience = "Yes" if "experience" in text.lower() else "No"

    return {
        "extracted_text": text[:1000],  # limit for preview
        "skills": skills,
        "has_experience": experience
    }
