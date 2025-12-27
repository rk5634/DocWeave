# ingestion/pdf_text_extractor.py

from pathlib import Path
import pdfplumber


class PDFTextExtractor:
    """
    Extracts text from digitally-generated PDFs (no OCR).
    """

    def extract(self, pdf_path: Path) -> str:
        text_pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)

        return "\n\n".join(text_pages).strip()
