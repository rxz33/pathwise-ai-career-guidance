# app/routes/upload_resume.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import mongo_service
from app.services.resume_parser import parse_resume

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(email: str = Form(...), resume: UploadFile = File(...)):
    try:
        file_bytes = await resume.read()
        parsed_data = parse_resume(file_bytes, resume.content_type)

        raw_resume = {"resume": {
            "extractedText": parsed_data.get("parsed_text_preview", ""),
            "skills": parsed_data.get("skills", []),
            "projects": parsed_data.get("projects", []),
            "certifications": parsed_data.get("certifications", []),
            "hasExperience": parsed_data.get("has_experience", "No")
        }}

        await mongo_service.update_user_by_email(email, {"rawResume": raw_resume})

        return {"message": "Resume uploaded successfully", "email": email, "rawResume": raw_resume}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
