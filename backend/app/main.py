from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import logger
from app.core.config import setup_cors
from app.database import create_indexes
from app.routes.submit_info import router as submit_info_router
from app.routes.cross_exam import router as cross_exam_router
from app.routes.tests import router as tests_router
from app.routes.upload_resume import router as upload_resume_router
from app.routes.final_analysis import router as final_analysis_router

app = FastAPI(
    title="AI Career Guidance System",
    version="1.0.0",
    description="API for cross-examining user data and generating career guidance using Gemini AI",
    debug=True
)

# Allow frontend origins
origins = [
    "https://pathwise-ai-career-guidance-ii0gkawoe.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Career Guide API!"}

# Include routes
app.include_router(submit_info_router)
app.include_router(cross_exam_router)
app.include_router(tests_router)
app.include_router(upload_resume_router)
app.include_router(final_analysis_router)

# Custom error handler
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Validation error: {exc.detail}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation failed", "details": exc.detail},
    )

@app.on_event("startup")
async def startup():
    await create_indexes()
