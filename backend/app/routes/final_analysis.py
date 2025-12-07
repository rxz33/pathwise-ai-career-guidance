# app/routes/finalize_career.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import asyncio
from app.services import mongo_service
from app.agents.gap_analyzer import GapAnalyzerAgent

router = APIRouter()

gap_agent = GapAnalyzerAgent()

# In-memory tasks store
tasks = {}

# --------------------- Request Schema ---------------------
class FinalizeCareerRequest(BaseModel):
    email: str

# --------------------- POST: Start Finalization ---------------------
@router.post("/finalize-career-path")
async def start_finalization(req: FinalizeCareerRequest):
    email = req.email

    # Fetch user data with all partial summaries
    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new task
    task_id = str(uuid4())
    tasks[task_id] = {"status": "running", "current_stage": 0, "partial_report": None}

    # Run finalization in background
    asyncio.create_task(run_finalization(task_id, user_data))
    return {"task_id": task_id}

# --------------------- GET: Check Status ---------------------
@router.get("/finalize-career-path/status/{task_id}")
async def get_finalization_status(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --------------------- Background Task ---------------------
async def run_finalization(task_id: str, user_data: dict):
    try:
        tasks[task_id]["current_stage"] = 0

        # ---------------- Step 1: Collect partial summaries ----------------
        partials = user_data.get("aiInsights", {}).get("partials", {})
        socio_summary = partials.get("socioEconomic", {})
        learning_summary = partials.get("learning", {})
        resume_summary = partials.get("resume", {})
        aptitude_summary = partials.get("aptitude", {})
        cross_summary = partials.get("crossExam", {})

        # ---------------- Step 2: Gap Analysis ----------------
        tasks[task_id]["current_stage"] = 1
        final_report = await gap_agent.generate_final_report(
            socio_summary,
            resume_summary,
            learning_summary,
            aptitude_summary,
            cross_summary,
            user_data.get("personalInfo", {}),
            user_data.get("optionalFields", {})
        )

        # ---------------- Step 3: Normalize lists for frontend ----------------
        for key in ["strengths", "weaknesses", "skill_gaps", "suggestions", "next_steps"]:
            val = final_report.get(key)
            if not isinstance(val, list):
                if isinstance(val, dict):
                    final_report[key] = list(map(str, val.values()))
                else:
                    final_report[key] = [str(val)] if val else []

        final_report["friendly_summary"] = str(final_report.get("friendly_summary", ""))

        tasks[task_id]["partial_report"] = {"final_report": final_report}
        tasks[task_id]["status"] = "completed"

        # ---------------- Step 4: Save final analysis in DB ----------------
        await mongo_service.update_final_analysis(user_data["email"], final_report)

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
