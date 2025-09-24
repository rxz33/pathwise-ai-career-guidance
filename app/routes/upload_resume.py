# app/routes/upload_resume.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import mongo_service
from app.services.resume_parser import parse_resume
from app.agents.resume_analyzer import ResumeAnalyzerAgent

router = APIRouter()
resume_agent = ResumeAnalyzerAgent()

@router.post("/upload-resume")
async def upload_resume(email: str = Form(...), resume: UploadFile = File(...)):
    try:
        file_bytes = await resume.read()
        parsed_data = parse_resume(file_bytes, resume.content_type)

        raw_resume = {
            "extractedText": parsed_data.get("parsed_text_preview", ""),
            "skills": parsed_data.get("skills", []),
            "projects": parsed_data.get("projects", []),
            "certifications": parsed_data.get("certifications", []),
            "hasExperience": parsed_data.get("has_experience", "No")
        }

        await mongo_service.update_user_by_email(email, {"rawResume": raw_resume})

        # Call Resume Analyzer agent only once
        resume_summary = await resume_agent.analyze_resume(
            parsed_data.get("parsed_text_preview", ""),
            strengths_and_weaknesses={}  # optional: can pull from DB
        )

        await mongo_service.update_user_by_email(email, {
            "aiInsights.partials.resume": resume_summary
        })

        return {"message": "Resume uploaded & analyzed", "email": email}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
