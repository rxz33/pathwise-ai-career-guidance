# app/routes/tests.py
from fastapi import APIRouter, HTTPException
from app.services import mongo_service
from app.schemas.user_data import BigFivePayload, RiasecPayload, AptiPayload

router = APIRouter()

@router.post("/big-five")
async def submit_big_five(payload: BigFivePayload):
    try:
        email = payload.email
        scores = payload.scores

        result = await mongo_service.update_user_by_email(
            email,
            {"tests": {"big_five": scores}}  # no $set here
        )

        if result.modified_count == 0 and not result.upserted_id:
            raise HTTPException(status_code=400, detail="Big Five result not stored")

        return {"message": "Big Five result stored successfully", "email": email, "scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/riasec")
async def submit_riasec(payload: RiasecPayload):
    try:
        email = payload.email
        scores = payload.scores

        result = await mongo_service.update_user_by_email(
            email,
            {"tests": {"riasec": scores}}
        )

        if result.modified_count == 0 and not result.upserted_id:
            raise HTTPException(status_code=400, detail="RIASEC result not stored")

        return {"message": "RIASEC result stored successfully", "email": email, "scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/apti")
async def submit_apti(payload: AptiPayload):
    try:
        email = payload.email
        scores = payload.scores

        result = await mongo_service.update_user_by_email(
            email,
            {"tests": {"apti": scores}}
        )

        if result.modified_count == 0 and not result.upserted_id:
            raise HTTPException(status_code=400, detail="APTI result not stored")

        return {"message": "APTI result stored successfully", "email": email, "scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
