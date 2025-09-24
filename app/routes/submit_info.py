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
        
        # Accept 'personal' instead of 'personalInfo'
        email = data.get("personal", {}).get("email")
        if not email:
            raise HTTPException(status_code=422, detail="Email is required")

        # Save raw user info
        await update_user_by_email(email, {"rawUserInfo": data})

        # Extract relevant data for agents
        personal_info = data.get("personal", {})
        optional_fields = data.get("optionalFields", {})
        strengths_and_weaknesses = data.get("strengthsAndWeaknesses", {})
        learning_roadmap = data.get("learningRoadmap", {})

        # Run agents in parallel
        socio_summary, learning_summary = await asyncio.gather(
            socio_agent.generate_summary(personal_info, optional_fields),
            learning_agent.analyze_learning(learning_roadmap, strengths_and_weaknesses)
        )

        # Save partial summaries
        await update_user_by_email(email, {
            "aiInsights.partials.socioEconomic": socio_summary,
            "aiInsights.partials.learning": learning_summary
        })

        return {"message": "User info stored & partial analysis done", "email": email}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
