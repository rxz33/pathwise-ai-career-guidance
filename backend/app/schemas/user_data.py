from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime

# ------------------- Personal Info -------------------
class PersonalInfos(BaseModel):
    fullName: Optional[str] = None
    age: Optional[int] = Field(None, ge=14, le=80)
    currentStatus: Optional[Literal["Student", "Fresher", "Working Professional", "Career Break"]] = None
    fieldOfStudy: Optional[str] = None
    educationLevel: Optional[
        Literal["High School", "Diploma/Intermediate", "Undergraduate", "Postgraduate", "Doctorate", "Other"]
    ] = None
    mobility: Optional[Literal["Willing to relocate", "Prefer hometown", "Depends on opportunity"]] = None
    financialStatus: Optional[Literal["Lower Class", "Middle Class", "Upper Class"]] = None

    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    class Config:
        extra = "allow"

# ------------------- Interests -------------------
class Interests(BaseModel):
    favoriteSubjects: Optional[str] = None
    favoriteSubjectsOther: Optional[str] = None

    activitiesThatMakeYouLoseTime: Optional[str] = None
    activitiesOther: Optional[str] = None

    onlineContent: Optional[str] = None
    onlineContentOther: Optional[str] = None

    exploreAreas: Optional[str] = None
    exploreAreasOther: Optional[str] = None

    preferredRole: Optional[str] = None
    preferredRoleOther: Optional[str] = None

    preferredCompany: Optional[str] = None
    preferredCompanyOther: Optional[str] = None

    jobPriorities: Optional[List[str]] = None
    jobPrioritiesOther: Optional[str] = None

    class Config:
        extra = "allow"

# ------------------- Strengths & Weaknesses -------------------
class StrengthWs(BaseModel):
    strengths: Optional[str] = None
    strengthsOther: Optional[str] = None

    struggleWith: Optional[str] = None
    struggleWithOther: Optional[str] = None

    confidenceLevel: Optional[int] = Field(None, ge=1, le=10)

    toolsTechUsed: Optional[str] = None
    toolsTechOther: Optional[str] = None

    internshipOrProject: Optional[str] = None
    internshipOther: Optional[str] = None

    whatDidYouLearn: Optional[str] = None
    learningOther: Optional[str] = None

    relatedToCareer: Optional[Literal["Yes", "No"]] = None

    hasResume: Optional[Literal["Yes", "No"]] = None
    resumeFile: Optional[bytes] = None  # For file upload

    class Config:
        extra = "allow"

# ------------------- Learning Roadmaps -------------------
class LearningRoadmaps(BaseModel):
    studyPlan: Optional[str] = None
    studyPlanOther: Optional[str] = None

    preferredLearning: Optional[str] = None
    preferredLearningOther: Optional[str] = None

    openToExplore: Optional[str] = None
    openToExploreOther: Optional[str] = None

    riskTaking: Optional[str] = None
    riskTakingOther: Optional[str] = None

    class Config:
        extra = "allow"

# ------------------- Optional Fields -------------------
class Optionals(BaseModel):
    currentRole: Optional[str] = None
    yearsOfExperience: Optional[int] = Field(None, ge=0, le=50)
    leadershipRole: Optional[Literal["Yes", "No"]] = None
    leadershipSkill: Optional[str] = None

    class Config:
        extra = "allow"

class BigFivePayload(BaseModel):
    email: EmailStr
    test: str | None = None
    scores: dict
    
class RiasecPayload(BaseModel):
    email: EmailStr
    test: str
    scores: dict
    
class AptiPayload(BaseModel):
    email: EmailStr
    test: str
    scores: dict
    
class Tests(BaseModel):
    bigFive: Optional[dict] = None
    riasec: Optional[dict] = None
    aptitude: Optional[dict] = None
    
# ------------------- Resume Data -------------------
class ResumeData(BaseModel):
    extractedText: Optional[str] = None
    skills: Optional[List[str]] = []
    projects: Optional[List[str]] = []
    certifications: Optional[List[str]] = []
    hasExperience: Optional[str] = None

    class Config:
        extra = "allow"

# ------------------- AI Insights (Agentic AI will fill this) -------------------
class AIInsights(BaseModel):
    consistencyReport: Optional[str] = None  # cross-check between resume & form & tests
    careerGaps: Optional[List[str]] = []
    personalizedRecommendations: Optional[List[str]] = []
    careerRoadmap: Optional[dict] = None

    class Config:
        extra = "allow"

# ------------------- Final Combined Model -------------------
class UserData(BaseModel):
    userId: Optional[str] = None
    email: Optional[EmailStr] = None  # ✅ added
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    personalInfo: Optional[PersonalInfos] = None
    interests: Optional[Interests] = None
    strengthsAndWeaknesses: Optional[StrengthWs] = None
    learningRoadmap: Optional[LearningRoadmaps] = None
    optionalFields: Optional[Optionals] = None

    # ✅ Resume Parsing Results
    resume: Optional[ResumeData] = None

    # ✅ Tests
    tests: Optional[Tests] = None

    # ✅ Agentic AI Results
    aiInsights: Optional[AIInsights] = None

    class Config:
        extra = "allow"


    
# ------------------- Cross Examination Input -------------------
class CrossExamInput(BaseModel):
    fullName: str
    age: Optional[int] = None
    currentStatus: Optional[str] = None
    fieldOfStudy: Optional[str] = None

    strengths: Optional[str] = None
    struggleWith: Optional[str] = None
    internshipOrProject: Optional[str] = None
    whatDidYouLearn: Optional[str] = None

    preferredRole: Optional[str] = None
    jobPriorities: Optional[List[str]] = None
    confidenceLevel: Optional[int] = None
    riskTaking: Optional[str] = None

class CrossExamEmail(BaseModel):
    email: EmailStr

    class Config:
        extra = "allow"
