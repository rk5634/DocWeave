# embeddings/embedder.py

from typing import List

from openai import OpenAI

from config.settings import OPENAI_API_KEY, EMBEDDING_MODEL


class Embedder:
    """
    Responsible for converting text into vector embeddings.
    """

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts,
        )

        return [item.embedding for item in response.data]
