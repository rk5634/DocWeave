# services/ingestion_service.py

from pathlib import Path
from typing import Union, BinaryIO

from ingestion.loader import DocumentLoader
from ingestion.ocr import DeepSeekOCR
from ingestion.text_cleaner import TextCleaner
from ingestion.chunker import TextChunker
from embeddings.vector_store import VectorStore


class IngestionService:
    """
    Orchestrates end-to-end document ingestion.
    """

    def __init__(self):
        self.loader = DocumentLoader()
        self.ocr = DeepSeekOCR()
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.vector_store = VectorStore()

    def ingest(self, file: Union[str, Path, BinaryIO]) -> dict:
        """
        Ingest a document into the RAG system.

        Steps:
        1. Load raw file
        2. OCR extraction
        3. Text cleaning
        4. Chunking
        5. Embedding + storage

        Returns a summary dict for UI or logging.
        """
        # 1. Load raw document
        raw_path = self.loader.load(file)

        # 2. OCR
        ocr_text_path = self.ocr.run(raw_path)

        # 3. Clean text
        cleaned_text_path = self.cleaner.clean(ocr_text_path)

        # 4. Chunk text
        chunks = self.chunker.chunk(cleaned_text_path)

        if not chunks:
            raise ValueError("No text chunks generated from document.")

        # 5. Store embeddings
        self.vector_store.add_documents(chunks)

        return {
            "status": "success",
            "source_file": str(raw_path),
            "ocr_text_file": str(ocr_text_path),
            "processed_text_file": str(cleaned_text_path),
            "num_chunks": len(chunks),
        }
