# config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

  
# Base Paths
  

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OCR_DATA_DIR = DATA_DIR / "ocr"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma"

# Ensure directories exist
for path in [
    DATA_DIR,
    RAW_DATA_DIR,
    OCR_DATA_DIR,
    PROCESSED_DATA_DIR,
    CHROMA_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)

  
# OpenAI Configuration
  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Please set it in your .env file."
    )

  
# Embedding Configuration
  

EMBEDDING_MODEL = "text-embedding-3-small"

  
# OCR Configuration (DeepSeek)
  

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise EnvironmentError(
        "DEEPSEEK_API_KEY not found. Please set it in your .env file."
    )

  
# ChromaDB Configuration
  

CHROMA_COLLECTION_NAME = "documents"

  
# RAG Parameters
  

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOP_K_RETRIEVAL = 5
MAX_GENERATION_RETRIES = 2
