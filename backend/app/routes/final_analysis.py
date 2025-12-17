from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4
import asyncio
from typing import Dict

from app.services import mongo_service
from app.agents.gap_analyzer import GapAnalyzerAgent

router = APIRouter()
gap_agent = GapAnalyzerAgent()

# --------------------- Request Schema ---------------------
class FinalizeCareerRequest(BaseModel):
    email: EmailStr


# --------------------- Helper: Force list ---------------------
def force_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    if isinstance(value, dict):
        return [str(v) for v in value.values() if v]
    if isinstance(value, str):
        return [value]
    return [str(value)]


# --------------------- POST: Start Finalization ---------------------
@router.post("/finalize-career-path")
async def start_finalization(req: FinalizeCareerRequest):
    email = req.email

    # 1. Fetch user
    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Create persistent task
    task_id = str(uuid4())

    await mongo_service.create_career_task({
        "_id": task_id,
        "email": email,
        "status": "running",
        "current_stage": 0,
        "partial_report": None,
        "error": None
    })

    # 3. Run background job
    asyncio.create_task(run_finalization(task_id, user_data))

    return {"task_id": task_id}


# --------------------- GET: Check Status ---------------------
@router.get("/finalize-career-path/status/{task_id}")
async def get_finalization_status(task_id: str):
    task = await mongo_service.get_career_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# --------------------- Background Task ---------------------
async def run_finalization(task_id: str, user_data: Dict):
    try:
        # ---------------- Step 1: Collect partial summaries ----------------
        await mongo_service.update_career_task(task_id, {
            "current_stage": 0
        })

        partials = user_data.get("aiInsights", {}).get("partials", {})

        socio_summary = partials.get("socioEconomic", {})
        learning_summary = partials.get("learning", {})
        resume_summary = partials.get("resume", {})
        aptitude_summary = partials.get("aptitude", {})
        cross_summary = partials.get("crossExam", {})

        # ---------------- Step 2: Build hard constraints ----------------
        constraints = {
            "risk_capacity": socio_summary.get("risk_capacity"),
            "restricted_career_types": socio_summary.get("restricted_career_types"),
            "allowed_career_types": socio_summary.get("allowed_career_types"),
            "resume_alignment": resume_summary.get("role_alignment"),
            "resume_risks": resume_summary.get("resume_risk_factors"),
            "aptitude_conflicts": aptitude_summary.get("conflicts"),
        }

        # ---------------- Step 3: Final Gap Analysis ----------------
        await mongo_service.update_career_task(task_id, {
            "current_stage": 1
        })

        final_report = await gap_agent.generate_final_report(
            socio_summary=socio_summary,
            resume_summary=resume_summary,
            learning_summary=learning_summary,
            aptitude_summary=aptitude_summary,
            cross_summary=cross_summary,
            personal_info=user_data.get("personalInfo", {}),
            optional_fields=user_data.get("optionalFields", {}),
            constraints=constraints
        )

        # ---------------- Step 4: HARD normalize for frontend ----------------

        final_report["friendly_summary"] = str(
            final_report.get("friendly_summary", "")
        )

        # Normalize simple list fields
        for key in ["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"]:
            final_report[key] = force_list(final_report.get(key))

        # CRITICAL FIX: normalize top_careers completely
        normalized_careers = []

        for career in final_report.get("top_careers", []):
            normalized_careers.append({
                "name": str(career.get("name", "Unknown Career")),
                "category": career.get("category", "SAFE"),
                "merits": force_list(career.get("merits")),
                "demerits": force_list(career.get("demerits")),
                "trends": force_list(career.get("trends")),
            })

        final_report["top_careers"] = normalized_careers

        final_report["_meta"] = {
            "generated_by": "GapAnalyzerAgent",
            "quality": "ok" if normalized_careers else "degraded"
        }

        # ---------------- Step 5: Persist results ----------------
        await mongo_service.update_final_analysis(
            user_data["email"],
            final_report
        )

        await mongo_service.update_career_task(task_id, {
            "status": "completed",
            "partial_report": {"final_report": final_report}
        })

    except Exception as e:
        await mongo_service.update_career_task(task_id, {
            "status": "failed",
            "error": str(e)
        })
