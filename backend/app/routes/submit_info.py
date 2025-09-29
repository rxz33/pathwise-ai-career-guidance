# app/routes/submit_info.py
from fastapi import APIRouter, Request, HTTPException
from app.services.mongo_service import update_user_by_email
import asyncio
from app.agents.socioeconomic_agent import SocioEconomicAgent
from app.agents.learning_roadmap_agent import LearningRoadmapAgent

router = APIRouter()

socio_agent = SocioEconomicAgent()
learning_agent = LearningRoadmapAgent()

@router.post("/submit-info")
async def submit_user_info(request: Request):
    try:
        data = await request.json()

        # Extract email safely
        email = data.get("personal", {}).get("email")
        if not email:
            raise HTTPException(status_code=422, detail="Email is required")

        # Save raw user info (optional)
        await update_user_by_email(email, {"rawUserInfo": data})

        # --- Selected fields for LearningRoadmapAgent ---
        learning_data = {k: data.get(k) for k in [
            "toolsTechUsed", "internshipOrProject", "relatedToCareer",
            "studyPlan", "preferredLearning", "openToExplore",
            "currentRole", "yearsOfExperience"
        ]}

        strengths_and_weaknesses = {
            "strengths": data.get("strengths"),
            "struggleWith": data.get("struggleWith"),
            "confidenceLevel": data.get("confidenceLevel")
        }

        # --- Selected fields for SocioEconomicAgent ---
        personal_info = {
            "name": data.get("personal", {}).get("name"),
            "email": email,
            "location": data.get("personal", {}).get("location"),
            "financialStatus": data.get("personal", {}).get("financialStatus")
        }

        optional_fields = {k: data.get(k) for k in [
            "favoriteSubjects", "activitiesThatMakeYouLoseTime",
            "onlineContent", "preferredRole", "preferredCompany", "jobPriorities"
        ]}

        # Run agents in parallel
        socio_summary, learning_summary = await asyncio.gather(
            socio_agent.generate_summary(personal_info, optional_fields),
            learning_agent.analyze_learning(learning_data, strengths_and_weaknesses, user_name=personal_info.get("name"))
        )

        # Save partial summaries
        await update_user_by_email(email, {
            "aiInsights.partials.socioEconomic": socio_summary,
            "aiInsights.partials.learning": learning_summary
        })

        return {"message": "User info stored & partial analysis done", "email": email}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
