from backend.services.ollama import ollama_service
from backend.prompts.templates import CLEANING_PROMPT, ANALYSIS_PROMPT
import json
import logging

logger = logging.getLogger(__name__)

async def clean_input(text: str) -> str:
    prompt = CLEANING_PROMPT.format(input_text=text)
    cleaned = await ollama_service.generate(prompt)
    return cleaned

async def analyze_intent(text: str) -> dict:
    prompt = ANALYSIS_PROMPT.format(input_text=text)
    response = await ollama_service.generate(prompt)
    
    try:
        if not response:
            logger.warning("Empty response from Ollama in analyze_intent")
            return {
                "survey_type": "General", "audience": "General", "industry": "Unknown",
                "goal": "Feedback", "sentiment": "Neutral", "tone": "Professional"
            }
            
        # Extract JSON if model added extra text
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
        return json.loads(response)
    except Exception as e:
        logger.error(f"Failed to parse analysis JSON: {e}")
        logger.debug(f"Raw response: {response}")
        return {
            "survey_type": "General",
            "audience": "General",
            "industry": "Unknown",
            "goal": "Feedback",
            "sentiment": "Neutral",
            "tone": "Professional"
        }
