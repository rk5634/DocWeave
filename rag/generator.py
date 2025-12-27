# rag/generator.py

from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from config.prompts import GENERATOR_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT


class GeneratorAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, question: str, documents: list, mode: str = "qa"):
        context = "\n\n".join(d["text"] for d in documents)

        system_prompt = (
            SUMMARY_SYSTEM_PROMPT if mode == "summary"
            else GENERATOR_SYSTEM_PROMPT
        )

        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nDocument:\n{context}",
                },
            ],
        )

        return {
            "answer": response.choices[0].message.content.strip(),
            "used_context": documents,
        }
