import httpx
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "phi3")

    async def generate(self, prompt: str, system: str = None) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_ctx": 4096,
                "top_p": 0.9,
            }
        }
        
        if system:
            payload["system"] = system

        logger.info(f"Sending request to Ollama (Model: {self.model})")
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                raw_response = data.get("response", "").strip()
                logger.info(f"Ollama response received. Length: {len(raw_response)}")
                return raw_response
        except Exception as e:
            logger.error(f"Ollama generation failed: {type(e).__name__}: {str(e)}")
            raise Exception(f"Ollama error: {str(e)}. Ensure Ollama is running.")

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False

ollama_service = OllamaService()
