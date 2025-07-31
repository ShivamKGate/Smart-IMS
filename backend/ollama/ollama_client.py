import requests

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model: str = "gemma3:latest"):
        self.base_url = base_url
        self.model = model

    def is_available(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags")
            return r.status_code == 200
        except:
            return False
    def text_to_sql(self, text):
        if not self.is_available():
            return "-- service not available"
        return "SELECT 1;"

ollama_client = OllamaClient()