# app/routes/tests.py
from fastapi import APIRouter, HTTPException
from app.services.mongo_service import update_user_by_email, get_user_by_email
from app.schemas.user_data import BigFivePayload, RiasecPayload, AptiPayload
from app.agents.interest_assessment_agent import AptitudeInterestAgent
import asyncio

router = APIRouter()
aptitude_agent = AptitudeInterestAgent()

async def save_test(email: str, test_name: str, scores: dict):
    update_data = {f"tests.{test_name}": scores}
    await update_user_by_email(email, update_data)
    return {test_name: scores}

async def analyze_aptitude(email: str):
    user_data = await get_user_by_email(email)
    tests = user_data.get("tests", {})
    interests = user_data.get("interests", {})
    summary = await aptitude_agent.analyze_tests(tests, interests)
    await update_user_by_email(email, {
        "aiInsights.partials.aptitude": summary
    })

@router.post("/big-five")
async def submit_big_five(payload: BigFivePayload):
    try:
        email = payload.email.strip().lower()
        print("Received payload:", payload.dict())

        # Prepare data to save: ensure personal.email exists and save test scores
        update_data = {
            "personal.email": email,
            "tests.big_five": payload.scores
        }

        # Atomic upsert: create if missing and update test scores
        await update_user_by_email(email, update_data, create_if_missing=True)
        print(f"Big Five test saved for {email}")

        # Run aptitude analysis after saving test
        await analyze_aptitude(email)
        print(f"Aptitude analysis completed for {email}")

        return {"message": "Big Five stored & analyzed", "email": email}

    except Exception as e:
        print("Error in /big-five:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/riasec")
async def submit_riasec(payload: RiasecPayload):
    try:
        await save_test(payload.email, "riasec", payload.scores)
        await analyze_aptitude(payload.email)
        return {"message": "RIASEC stored & analyzed", "email": payload.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apti")
async def submit_apti(payload: AptiPayload):
    try:
        await save_test(payload.email, "aptitude", payload.scores)
        await analyze_aptitude(payload.email)
        return {"message": "Aptitude stored & analyzed", "email": payload.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
