# rag/validator.py

import json
from typing import List, Dict

from openai import OpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from config.prompts import VALIDATOR_SYSTEM_PROMPT


class ValidatorAgent:
    """
    Validates whether a generated answer is fully supported
    by the retrieved document context.
    """

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def validate(
        self,
        question: str,
        answer: str,
        documents: List[Dict],
    ) -> Dict:
        """
        Validate the generated answer against the source documents.
        """
        if not answer:
            return {
                "is_valid": False,
                "reason": "Empty answer.",
            }

        context = self._build_context(documents)

        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": VALIDATOR_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(
                        question=question,
                        answer=answer,
                        context=context,
                    ),
                },
            ],
            temperature=0.0,
        )

        raw_output = response.choices[0].message.content.strip()

        return self._parse_validation_output(raw_output)

    @staticmethod
    def _build_context(documents: List[Dict]) -> str:
        """
        Build context block for validation.
        """
        blocks = []

        for idx, doc in enumerate(documents, start=1):
            blocks.append(
                f"[Document {idx}]\n{doc['text']}"
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _build_user_prompt(
        question: str,
        answer: str,
        context: str,
    ) -> str:
        """
        Construct the validation prompt.
        """
        return f"""
User Question:
{question}

Generated Answer:
{answer}

Document Context:
{context}

Evaluate the answer strictly against the document context
and respond ONLY with the required JSON format.
""".strip()

    @staticmethod
    def _parse_validation_output(output: str) -> Dict:
        """
        Safely parse validator output into structured JSON.
        """
        try:
            parsed = json.loads(output)

            if "is_valid" not in parsed:
                raise ValueError("Missing 'is_valid' field")

            return {
                "is_valid": bool(parsed["is_valid"]),
                "reason": parsed.get("reason", ""),
            }

        except Exception:
            # Fail-safe: treat unparseable output as invalid
            return {
                "is_valid": False,
                "reason": "Validator output was not valid JSON.",
            }
