from backend.services.ollama import ollama_service
from backend.prompts.templates import GENERATION_PROMPT
import json
import logging

logger = logging.getLogger(__name__)

async def generate_survey_content(cleaned_text: str, analysis: dict) -> dict:
    prompt = GENERATION_PROMPT.format(
        cleaned_text=cleaned_text,
        survey_type=analysis.get("survey_type", "General"),
        audience=analysis.get("audience", "General"),
        industry=analysis.get("industry", "Unknown"),
        goal=analysis.get("goal", "Feedback"),
        tone=analysis.get("tone", "Professional")
    )
    
    response = await ollama_service.generate(prompt)
    
    try:
        if not response:
            raise Exception("Empty response from Ollama during survey generation.")

        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
        return json.loads(response)
    except Exception as e:
        logger.error(f"Failed to parse generation JSON: {e}")
        logger.debug(f"Raw response: {response}")
        raise Exception(f"Failed to generate structured survey: {str(e)}")
