# app/routes/upload_resume.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import mongo_service
from app.services.resume_parser import parse_resume  # import the parser

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(email: str = Form(...), resume: UploadFile = File(...)):
    try:
        # ✅ Read file bytes
        file_content = await resume.read()

        # ✅ Parse resume using the centralized parser service
        parsed_data = parse_resume(file_content, resume.content_type)

        # ✅ Prepare data to store in MongoDB
        resume_data = {
            "resume": {
                "filename": resume.filename,
                "content_type": resume.content_type,
                "data": file_content,
                "parsed_text": parsed_data["extracted_text"],
                "skills": parsed_data.get("skills", []),
                "has_experience": parsed_data.get("has_experience", "No")
            }
        }

        # ✅ Update user document
        result = await mongo_service.update_user_by_email(email, resume_data)

        if result.modified_count == 0 and result.upserted_id is None:
            raise HTTPException(status_code=400, detail="Resume upload failed")

        return {
            "message": "Resume uploaded & parsed successfully",
            "email": email,
            "parsed_text_preview": parsed_data["extracted_text"][:300],  # preview first 300 chars
            "skills": parsed_data.get("skills", []),
            "has_experience": parsed_data.get("has_experience", "No")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
