# app/routes/tests.py
from fastapi import APIRouter, HTTPException
from app.services import mongo_service
from app.schemas.user_data import BigFivePayload, RiasecPayload, AptiPayload
from app.agents.interest_assessment_agent import AptitudeInterestAgent
import asyncio

router = APIRouter()
aptitude_agent = AptitudeInterestAgent()

async def save_test(email: str, test_name: str, scores: dict):
    update_data = {f"tests.{test_name}": scores}
    await mongo_service.update_user_by_email(email, update_data)
    return {test_name: scores}

async def analyze_aptitude(email: str):
    user_data = await mongo_service.get_user_by_email(email)
    tests = user_data.get("tests", {})
    interests = user_data.get("interests", {})
    summary = await aptitude_agent.analyze_tests(tests, interests)
    await mongo_service.update_user_by_email(email, {
        "aiInsights.partials.aptitude": summary
    })

# @router.post("/big-five")
# async def submit_big_five(payload: BigFivePayload):
#     try:
#         await save_test(payload.email, "bigFive", payload.scores)
#         await analyze_aptitude(payload.email)
#         return {"message": "Big Five stored & analyzed", "email": payload.email}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/big-five")
async def submit_big_five(payload: BigFivePayload):
    try:
        print("Received payload:", payload.dict())  # log payload
        saved = await save_test(payload.email, "bigFive", payload.scores)
        print("Saved test:", saved)
        await analyze_aptitude(payload.email)
        return {"message": "Big Five stored & analyzed", "email": payload.email}
    except Exception as e:
        print("Error in /big-five:", str(e))  # log full error
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
