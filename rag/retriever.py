# rag/retriever.py

from embeddings.vector_store import VectorStore
from config.settings import TOP_K_RETRIEVAL


class RetrieverAgent:
    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, mode: str = "qa"):
        """
        mode:
          - qa: retrieve top-k relevant chunks
          - summary: retrieve many representative chunks
        """
        if mode == "summary":
            # Pull more context for summaries
            return self.vector_store.retrieve(query, k=20)

        return self.vector_store.retrieve(query, k=TOP_K_RETRIEVAL)
