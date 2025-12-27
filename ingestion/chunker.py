# ingestion/chunker.py

from pathlib import Path
from typing import List, Dict

from config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    PROCESSED_DATA_DIR,
)


class TextChunker:
    """
    Splits cleaned text into semantically meaningful chunks
    suitable for embedding.
    """

    def chunk(self, cleaned_text_path: Path) -> List[Dict]:
        """
        Main entry point.
        Returns a list of chunk dictionaries.
        """
        cleaned_text_path = Path(cleaned_text_path)

        if not cleaned_text_path.exists():
            raise FileNotFoundError(
                f"Cleaned text file not found: {cleaned_text_path}"
            )

        text = cleaned_text_path.read_text(encoding="utf-8")

        paragraphs = self._split_into_paragraphs(text)
        chunks = self._build_chunks(paragraphs)

        return self._attach_metadata(
            chunks=chunks,
            source=str(cleaned_text_path),
        )

    @staticmethod
    def _split_into_paragraphs(text: str) -> List[str]:
        """
        Split text into paragraphs using double line breaks.
        """
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    def _build_chunks(self, paragraphs: List[str]) -> List[str]:
        """
        Build chunks using paragraph-aware sliding window.
        """
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length = 0

        for para in paragraphs:
            para_length = len(para)

            # If paragraph itself is too large, split it
            if para_length > CHUNK_SIZE:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_length = 0

                chunks.extend(self._split_large_text(para))
                continue

            if current_length + para_length <= CHUNK_SIZE:
                current_chunk.append(para)
                current_length += para_length
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [para]
                current_length = para_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return self._apply_overlap(chunks)

    def _split_large_text(self, text: str) -> List[str]:
        """
        Split very large paragraphs using a sliding window.
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - CHUNK_OVERLAP

        return chunks

    @staticmethod
    def _apply_overlap(chunks: List[str]) -> List[str]:
        """
        Ensures consistent formatting and removes empty chunks.
        """
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    @staticmethod
    def _attach_metadata(
        chunks: List[str],
        source: str,
    ) -> List[Dict]:
        """
        Attach metadata required for embeddings and retrieval.
        """
        return [
            {
                "text": chunk,
                "metadata": {
                    "source": source,
                    "chunk_index": idx,
                },
            }
            for idx, chunk in enumerate(chunks)
        ]
