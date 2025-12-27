# ingestion/text_cleaner.py

import re
from pathlib import Path
from config.settings import PROCESSED_DATA_DIR


class TextCleaner:
    """
    Cleans OCR text with English-only normalization.
    """

    def clean(self, ocr_text_path: Path) -> Path:
        raw_text = ocr_text_path.read_text(encoding="utf-8", errors="ignore")

        text = self._remove_non_english(raw_text)
        text = self._fix_hyphenation(text)
        text = self._normalize_whitespace(text)
        text = self._remove_noise_lines(text)

        output_path = PROCESSED_DATA_DIR / ocr_text_path.name
        output_path.write_text(text.strip(), encoding="utf-8")

        return output_path

    @staticmethod
    def _remove_non_english(text: str) -> str:
        """
        Remove non-English Unicode characters.
        """
        return re.sub(r"[^\x00-\x7F]+", " ", text)

    @staticmethod
    def _fix_hyphenation(text: str) -> str:
        return re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    @staticmethod
    def _remove_noise_lines(text: str) -> str:
        lines = []
        for line in text.split("\n"):
            line = line.strip()
            if len(line) < 3:
                continue
            if not re.search(r"[a-zA-Z]", line):
                continue
            lines.append(line)
        return "\n".join(lines)
