# services/intent_service.py

import json
from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from config.prompts import INTENT_CLASSIFIER_PROMPT


class IntentService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def classify(self, question: str) -> dict:
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.0,
            messages=[
                {"role": "system", "content": INTENT_CLASSIFIER_PROMPT},
                {"role": "user", "content": question},
            ],
        )

        try:
            return json.loads(response.choices[0].message.content.strip())
        except Exception:
            return {"intent": "document"}
