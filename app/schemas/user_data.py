from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

class PersonalInfos(BaseModel):
    fullName: Optional[str]
    age: Optional[int] = Field(None, ge=14, le=80)
    currentStatus: Optional[Literal["Student", "Fresher", "Working Professional", "Career Break"]]
    fieldOfStudy: Optional[str]
    educationLevel: Optional[
        Literal["High School", "Diploma/Intermediate", "Undergraduate", "Postgraduate", "Doctorate", "Other"]
    ]
    mobility: Optional[Literal["Willing to relocate", "Prefer hometown", "Depends on opportunity"]]
    financialStatus: Optional[int] = Field(None, ge=1, le=10)

    class Config:
        extra = "allow"

class Interests(BaseModel):
    favoriteSubjects: Optional[str]
    activitiesThatMakeYouLoseTime: Optional[str]
    onlineContent: Optional[str]
    exploreAreas: Optional[str]
    preferredRole: Optional[str]
    preferredCompany: Optional[str]
    jobPriorities: Optional[List[str]]

    class Config:
        extra = "allow"

class StrengthWs(BaseModel):
    strengths: Optional[str]
    struggleWith: Optional[str]
    confidenceLevel: Optional[int] = Field(None, ge=1, le=10)
    toolsTechUsed: Optional[str]
    internshipOrProject: Optional[str]
    whatDidYouLearn: Optional[str]
    relatedToCareer: Optional[Literal["Yes", "No"]]

    class Config:
        extra = "allow"

class LearningRoadmaps(BaseModel):
    studyPlan: Optional[str]
    preferredLearning: Optional[List[str]]
    openToExplore: Optional[Literal["Yes", "No"]]
    riskTaking: Optional[Literal["Low", "Medium", "High"]]

    class Config:
        extra = "allow"

class Optionals(BaseModel):
    currentRole: Optional[str] = None
    yearsOfExperience: Optional[int] = Field(None, ge=0, le=50) 
    leadershipRole: Optional[Literal["Yes", "No"]] = None
    leadershipSkill: Optional[str] = None

    class Config:
        extra = "allow"

# Final combined model
class UserData(BaseModel):
    personalInfo: Optional[PersonalInfos] = None
    interests: Optional[Interests] = None
    strengthsAndWeaknesses: Optional[StrengthWs] = None
    learningRoadmap: Optional[LearningRoadmaps] = None
    optionalFields: Optional[Optionals] = None
    
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
