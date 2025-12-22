from fastapi import FastAPI, Request, HTTPException  #“FastAPI is a Python web framework implemented as a package that provides modules, classes, and functions for building APIs.”
from fastapi.responses import JSONResponse      #fastapi-package, fastapi.respones-modules(files), JSONResponse-Class
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import logger   #server-side debugging
from app.database import create_indexes
from app.routes.submit_info import router as submit_info_router  #features
from app.routes.cross_exam import router as cross_exam_router
from app.routes.tests import router as tests_router
from app.routes.upload_resume import router as upload_resume_router
from app.routes.final_analysis import router as final_analysis_router

app = FastAPI(         #server brain object/instance and app is a FastAPI application object and ASGI server(uvicorn) runs the app.
    title="AI Career Guidance System",  #sets the API name used in swagger ui/ openapi docs
    version="1.0.0",         #sets API version and helps track releases, versioning and maintenance
    description="API for cross-examining user data and generating career guidance using AI",  #explain what api does , shown in documentation
    debug=True     #shows detailed error traces, helps during development, true- dev only, false-production
)

origins = [
    "https://pathwise-ai-career-guidance-ii0gkawoe.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

#CORS preflight options - check is origin, method or headers allowed

app.add_middleware(
    CORSMiddleware,  #registering built in middleware and it will run for every request
    allow_origins=origins,      
    allow_credentials=True,  #frontend can send cookies, authorization headers, tokens
    allow_methods=["*"],  #allow all methods, get, post, put, delete, and OPTIONS very imp for CORS
    allow_headers=["*"],   #allow all headers, content-type, authorization and content headers, without this, many apis break
)

# Default route - for simple API check and monitoring 
@app.get("/")  #route is not called it is registered, and fastapi call later when request arrives 
async def read_root():
    return {"message": "Welcome to the AI Career Guide API!"}  #dict

# Include routes
app.include_router(submit_info_router)
app.include_router(cross_exam_router)
app.include_router(tests_router)
app.include_router(upload_resume_router)
app.include_router(final_analysis_router)

# Custom error handler, 5consistent error format 422-unprocessable entity
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Validation error: {exc.detail}")    #helps debugging and logs error internally 
    return JSONResponse(
        status_code=422,
        content={"message": "Validation failed", "details": exc.detail},
    )

@app.on_event("startup")
async def startup():
    await create_indexes()  #first start app. then prepare database, then accepts requests

# 1. Python loads this file
# 2. Imports are executed
# 3. app = FastAPI() is created
# 4. Middleware is registered
# 5. Routes are registered (@app.get, include_router)
# 6. Exception handlers are registered
# 7. Startup events are registered (NOT executed yet)
# 8. Uvicorn starts the server
# 9. FastAPI fires startup events
#    → create_indexes() runs
# 10. Application starts accepting requests
