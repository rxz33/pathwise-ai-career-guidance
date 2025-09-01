# app/routes/upload_resume.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import mongo_service
import PyPDF2
import docx
import io

router = APIRouter()

def parse_resume(file_bytes: bytes, content_type: str) -> str:
    """
    Extract text from PDF or DOCX resumes.
    """
    text = ""
    try:
        if content_type == "application/pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text += page.extract_text() or ""
        elif content_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]:
            doc = docx.Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = ""  # unsupported format (optional: raise exception)
    except Exception as e:
        text = f"Error parsing resume: {str(e)}"
    return text.strip()

@router.post("/upload_resume")
async def upload_resume(email: str = Form(...), resume: UploadFile = File(...)):
    try:
        # ✅ Read file bytes
        file_content = await resume.read()

        # ✅ Parse resume text
        extracted_text = parse_resume(file_content, resume.content_type)

        # ✅ Prepare data to store
        resume_data = {
            "resume": {
                "filename": resume.filename,
                "content_type": resume.content_type,
                "data": file_content,
                "parsed_text": extracted_text
            }
        }

        # ✅ Update user document
        result = await mongo_service.update_user_by_email(email, resume_data)

        if result.modified_count == 0 and result.upserted_id is None:
            raise HTTPException(status_code=400, detail="Resume upload failed")

        return {
            "message": "Resume uploaded & parsed successfully",
            "email": email,
            "parsed_text_preview": extracted_text[:300]  # preview first 300 chars
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
