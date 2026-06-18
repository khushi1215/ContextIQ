import requests
from backend.config import settings
class AnswerGenerator:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,
    ) -> None:

        self.model = model

        self.url = settings.OLLAMA_URL

    def build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the prompt sent to Ollama.
        """

        prompt = f"""
You are an AI assistant for document question answering.

Rules:

- Answer ONLY using the document context below.
- Do NOT use outside knowledge.
- If the answer is not explicitly present, reply exactly:

The requested information is not available in the provided document.

- Quote important facts from the document.
- Keep answers concise (3–6 sentences).
- Never guess.

=========================
DOCUMENT
=========================

{context}

=========================
QUESTION
=========================

{query}

=========================
ANSWER
=========================
"""

        return prompt

    def generate(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate an answer using Ollama.
        """

        prompt = self.build_prompt(
            query,
            context,
        )
        print(f"Using model: {self.model}")
        print(f"Prompt length: {len(prompt)}")

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 200,},
            },
            timeout=120,
        )

        if response.status_code != 200:
            print("\nOLLAMA ERROR")
            print(response.status_code)
            print(response.text)
            response.raise_for_status()

        data = response.json()

        return data["response"].strip()