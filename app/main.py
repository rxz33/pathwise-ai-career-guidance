from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.core.config import setup_cors
from app.database import create_indexes
from fastapi.middleware.cors import CORSMiddleware
from app.routes.submit_info import router as submit_info_router
# from app.routes.cross_exam import router as cross_exam_router
# from app.routes.career_result import router as career_result_router
# from app.routes.evaluate_cross_exam import router as evaluate_cross_exam_router
from app.routes.result import router as result_router
from app.routes.tests import router as tests_router
from app.routes.upload_resume import router as upload_resume_router
# from app.routes.pipeline_routes import router as pipeline_router
from app.routes.clean_profile import router as clean_router

app = FastAPI(
    title="AI Career Guidance System",
    version="1.0.0",
    description="API for cross-examining user data and generating career guidance using Gemini AI",
    debug=True
)

# CORS setup
setup_cors(app)

# Allow your frontend origin
origins = [
    "http://localhost:5173",  # frontend dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # allow headers like Content-Type
)

# Default route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Career Guide API!"}

# Include routes
app.include_router(submit_info_router)
# app.include_router(cross_exam_router)
# app.include_router(career_result_router)
# app.include_router(evaluate_cross_exam_router)

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

app.include_router(result_router)
app.include_router(tests_router)
app.include_router(upload_resume_router)
app.include_router(clean_router)
# app.include_router(pipeline_router)