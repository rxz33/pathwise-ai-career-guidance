from pydantic import BaseModel
from typing import List

class CrossExamQuestionSet(BaseModel):
    questions: List[str]

class CrossExamAnswerInput(BaseModel):
    email: str
    evaluation: str
