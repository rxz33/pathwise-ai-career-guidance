# app/routes/tests.py
from fastapi import APIRouter, HTTPException
from app.services import mongo_service
from app.schemas.user_data import BigFivePayload, RiasecPayload, AptiPayload

router = APIRouter()

async def save_test(email: str, test_name: str, scores: dict):
    """
    Save test under 'tests' object in user document without overwriting existing tests.
    """
    update_data = {f"tests.{test_name}": scores}  # dot notation merges
    await mongo_service.update_user_by_email(email, update_data)
    return {test_name: scores}

@router.post("/big-five")
async def submit_big_five(payload: BigFivePayload):
    try:
        result = await save_test(payload.email, "bigFive", payload.scores)
        return {"message": "Big Five result stored", "email": payload.email, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/riasec")
async def submit_riasec(payload: RiasecPayload):
    try:
        result = await save_test(payload.email, "riasec", payload.scores)
        return {"message": "RIASEC result stored", "email": payload.email, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apti")
async def submit_apti(payload: AptiPayload):
    try:
        result = await save_test(payload.email, "aptitude", payload.scores)
        return {"message": "APTI result stored", "email": payload.email, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
