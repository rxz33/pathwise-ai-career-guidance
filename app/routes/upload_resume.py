# app/routes/upload_resume.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import mongo_service
from app.services.resume_parser import parse_resume
from app.schemas.user_data import ResumeData  # ✅ import your Pydantic model

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(email: str = Form(...), resume: UploadFile = File(...)):
    print("Received email:", email)
    print("Received file:", resume.filename, resume.content_type)
    
    try:
        # ✅ Read file bytes
        file_content = await resume.read()

        # ✅ Parse resume
        parsed_data = parse_resume(file_content, resume.content_type)

        # ✅ Validate with ResumeData schema
        resume_model = ResumeData(**parsed_data)

        # ✅ Prepare data for MongoDB
        resume_data = {
    "resume": {
        "extractedText": parsed_data.get("parsed_text_preview", ""),
        "skills": parsed_data.get("skills", []),
        "projects": parsed_data.get("projects", []),
        "certifications": parsed_data.get("certifications", []),
        "hasExperience": parsed_data.get("has_experience", "No")
    }
}
        # ✅ Update user document
        result = await mongo_service.update_user_by_email(email, resume_data)

        if result.modified_count == 0 and result.upserted_id is None:
            raise HTTPException(status_code=400, detail="Resume upload failed")

        return {
            "message": "Resume uploaded & parsed successfully",
            "email": email,
            "parsed_text_preview": resume_model.extractedText[:300] if resume_model.extractedText else "",
            "skills": resume_model.skills,
            "projects": resume_model.projects,
            "certifications": resume_model.certifications,
            "has_experience": resume_model.hasExperience,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
