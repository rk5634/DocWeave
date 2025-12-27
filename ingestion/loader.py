# ingestion/loader.py

from pathlib import Path
from typing import Union, BinaryIO
import shutil
import pdfplumber

from config.settings import RAW_DATA_DIR


class DocumentLoader:
    """
    Loads uploaded documents and detects if OCR is required.
    """

    def load(self, file: Union[str, Path, BinaryIO]) -> Path:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        if hasattr(file, "read"):  # Streamlit upload
            output_path = RAW_DATA_DIR / file.name
            with open(output_path, "wb") as f:
                f.write(file.read())
        else:
            file = Path(file)
            output_path = RAW_DATA_DIR / file.name
            shutil.copy(file, output_path)

        return output_path

    @staticmethod
    def is_text_pdf(pdf_path: Path) -> bool:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:2]:
                    if page.extract_text():
                        return True
        except Exception:
            pass
        return False
