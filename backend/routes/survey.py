from fastapi import APIRouter, Depends, HTTPException
from backend.models.schemas import SurveyGenerationRequest, SurveyResponse, AnalysisResult, HealthResponse
from backend.services.analyzer import clean_input, analyze_intent
from backend.services.generator import generate_survey_content
from backend.services.validator import validate_and_deduplicate
from backend.services.ollama import ollama_service
from backend.database.db import get_db, SurveyRecord
from sqlalchemy.orm import Session
import json

router = APIRouter()

@router.post("/generate-survey", response_model=SurveyResponse)
async def generate_survey(request: SurveyGenerationRequest, db: Session = Depends(get_db)):
    try:
        # 1. Clean Input
        cleaned_text = await clean_input(request.raw_text)
        
        # 2. Analyze Intent
        analysis = await analyze_intent(cleaned_text)
        
        # 3. Generate Content
        survey_content = await generate_survey_content(cleaned_text, analysis)
        
        # 4. Validate and Deduplicate
        final_survey = validate_and_deduplicate(survey_content)
        
        # 5. Save to Database
        db_record = SurveyRecord(
            title=final_survey["title"],
            description=final_survey["description"],
            questions=final_survey["questions"],
            raw_input=request.raw_text,
            metadata_json=analysis
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return {
            "id": db_record.id,
            "title": db_record.title,
            "description": db_record.description,
            "questions": db_record.questions,
            "metadata": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-input", response_model=AnalysisResult)
async def analyze_input_route(request: SurveyGenerationRequest):
    cleaned = await clean_input(request.raw_text)
    analysis = await analyze_intent(cleaned)
    return analysis

@router.get("/health", response_model=HealthResponse)
async def health_check():
    ollama_status = await ollama_service.check_health()
    return {
        "status": "ok",
        "ollama_connected": ollama_status
    }
