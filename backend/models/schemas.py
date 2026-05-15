from pydantic import BaseModel, Field
from typing import List, Optional, Any

class QuestionBase(BaseModel):
    type: str = Field(..., description="Type of question: rating, multiple_choice, yes_no, open_ended")
    question: str = Field(..., description="The survey question text")
    options: Optional[List[str]] = Field(None, description="List of options for multiple choice questions")

class SurveyBase(BaseModel):
    title: str
    description: str
    questions: List[QuestionBase]

class SurveyGenerationRequest(BaseModel):
    raw_text: str = Field(..., min_length=10)

class AnalysisResult(BaseModel):
    survey_type: str
    audience: str
    industry: str
    goal: str
    sentiment: str
    tone: str

class ProcessedInput(BaseModel):
    original_text: str
    cleaned_text: str
    analysis: AnalysisResult

class SurveyResponse(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    questions: List[QuestionBase]
    metadata: Optional[dict] = None

class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
