import os
from abc import ABC, abstractmethod
from typing import Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv()

class VisionProvider(ABC):
    @abstractmethod
    def verify_evidence(self, image_bytes: bytes, objective_description: str) -> Dict[str, Any]:
        """Analyzes an image to see if it fulfills an objective."""
        pass

class OllamaVisionProvider(VisionProvider):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("VISION_MODEL", "llava")

    def verify_evidence(self, image_bytes: bytes, objective_description: str) -> Dict[str, Any]:
        import base64
        import json
        import logging
        import re
        logger = logging.getLogger("questme")

        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        prompt = f"""Analyze this image for the following objective: '{objective_description}'.
Return ONLY a JSON object with these exact keys:
{{
  "valid": boolean,
  "confidence": float (0.0 to 1.0),
  "reason": "brief explanation"
}}
Do not include any conversational text, markdown code blocks, or explanations outside the JSON."""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "images": [image_b64],
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            raw_response = result.get("response", "").strip()
            if not raw_response:
                return {"valid": False, "confidence": 0.0, "reason": "AI returned an empty response"}

            # Robust JSON extraction: find the first { and last }
            try:
                start_idx = raw_response.find('{')
                end_idx = raw_response.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_str = raw_response[start_idx:end_idx + 1]
                    return json.loads(json_str)

                # If no braces found, the model failed to provide JSON
                return {"valid": False, "confidence": 0.0, "reason": f"AI failed to provide JSON response: {raw_response[:100]}..."}
            except json.JSONDecodeError:
                logger.error(f"Failed to decode AI response as JSON: {raw_response}")
                return {"valid": False, "confidence": 0.0, "reason": "AI provided malformed JSON"}

        except Exception as e:
            logger.error(f"VisionProvider Error: {e}")
            return {"valid": False, "confidence": 0.0, "reason": "Vision service currently unavailable"}

def get_vision_provider() -> VisionProvider:
    # Currently only supporting Ollama for vision
    return OllamaVisionProvider()
