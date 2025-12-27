# embeddings/vector_store.py

from typing import List, Dict
import chromadb

from embeddings.embedder import Embedder
from config.settings import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
    TOP_K_RETRIEVAL,
)


class VectorStore:
    _client = None
    _collection = None

    def __init__(self):
        if VectorStore._client is None:
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)

            VectorStore._client = chromadb.PersistentClient(
                path=str(CHROMA_DIR)
            )

            VectorStore._collection = (
                VectorStore._client.get_or_create_collection(
                    name=CHROMA_COLLECTION_NAME
                )
            )

        self._client = VectorStore._client
        self._collection = VectorStore._collection
        self._embedder = Embedder()

    def add_documents(self, chunks: List[Dict]) -> None:
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [
            f"{c['metadata']['source']}::{c['metadata']['chunk_index']}"
            for c in chunks
        ]

        embeddings = self._embedder.embed_texts(texts)

        self._collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )


    def retrieve(self, query: str, k: int = TOP_K_RETRIEVAL) -> List[Dict]:
        query_embedding = self._embedder.embed_texts([query])[0]

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return [
            {"text": doc, "metadata": meta}
            for doc, meta in zip(documents, metadatas)
        ]
