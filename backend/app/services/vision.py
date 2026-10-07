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
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        prompt = f"Does this image provide reasonable evidence for the following objective: '{objective_description}'? Return ONLY a JSON object with 'valid' (boolean), 'confidence' (float 0-1), and 'reason' (string)."

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
            import json
            return json.loads(result.get("response", '{"valid": false, "reason": "No response from AI"}'))
        except Exception as e:
            print(f"VisionProvider Error: {e}")
            return {"valid": False, "confidence": 0.0, "reason": f"Error: {str(e)}"}

def get_vision_provider() -> VisionProvider:
    # Currently only supporting Ollama for vision
    return OllamaVisionProvider()
