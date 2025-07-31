import requests
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model: str = "gemma3:latest"):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()

    def is_available(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags")
            return r.status_code == 200
        except:
            return False

    def text_to_sql(self, user_input: str) -> str:
        if not self.is_available():
            return f"-- Error: Ollama not available"
        prompt = self._build_prompt(user_input)
        resp = self.session.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=20
        )
        data = resp.json()
        sql = self._clean_sql(data.get("response", ""))
        return sql

    def _build_prompt(self, text: str) -> str:
        return f"Convert to SQL: {text}\n"

    def _clean_sql(self, sql: str) -> str:
        lines = [l.strip() for l in sql.splitlines() if l.strip()]
        script = " ".join(lines)
        return script if script.endswith(";") else script + ";"

ollama_client = OllamaClient()