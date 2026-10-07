import os
from abc import ABC, abstractmethod
from typing import Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv()

class BaseInferenceProvider(ABC):
    @abstractmethod
    def generate_json(self, prompt: str, schema_name: str) -> Dict[str, Any]:
        """Generates a JSON response based on a prompt and a schema name."""
        pass

class OllamaProvider(BaseInferenceProvider):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("QUEST_MODEL", "qwen3-coder:480b-cloud")

    def generate_json(self, prompt: str, schema_name: str) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            import json
            return json.loads(result.get("response", "{}"))
        except Exception as e:
            print(f"OllamaProvider Error: {e}")
            raise e

class CloudProvider(BaseInferenceProvider):
    """
    Placeholder for a cloud-based inference provider (e.g., OpenAI-compatible API).
    Used when INFERENCE_MODE=cloud.
    """
    def __init__(self):
        self.api_key = os.getenv("CLOUD_AI_API_KEY")
        self.base_url = os.getenv("CLOUD_AI_BASE_URL")
        self.model = os.getenv("CLOUD_AI_MODEL")

    def generate_json(self, prompt: str, schema_name: str) -> Dict[str, Any]:
        # Implementation for OpenAI-compatible API would go here
        raise NotImplementedError("CloudProvider not yet implemented. Use INFERENCE_MODE=ollama")

def get_inference_provider() -> BaseInferenceProvider:
    mode = os.getenv("INFERENCE_MODE", "ollama").lower()
    if mode == "ollama":
        return OllamaProvider()
    elif mode == "cloud":
        return CloudProvider()
    else:
        raise ValueError(f"Unsupported INFERENCE_MODE: {mode}")
