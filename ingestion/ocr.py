# ingestion/ocr.py

from pathlib import Path
from openai import OpenAI
from PIL import Image
from pdf2image import convert_from_path

from ingestion.image_preprocessor import ImagePreprocessor
from ingestion.pdf_text_extractor import PDFTextExtractor
from ingestion.loader import DocumentLoader
from config.settings import DEEPSEEK_API_KEY, OCR_DATA_DIR


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepinfra.com/v1/openai",
)

OCR_MODEL = "deepseek-ai/DeepSeek-OCR"


class DeepSeekOCR:
    """
    OCR pipeline with smart PDF detection.
    """

    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.pdf_text_extractor = PDFTextExtractor()

    def run(self, file_path: Path) -> Path:
        file_path = Path(file_path)
        OCR_DATA_DIR.mkdir(parents=True, exist_ok=True)

        # ✅ If PDF has text → extract directly
        if file_path.suffix.lower() == ".pdf" and DocumentLoader.is_text_pdf(file_path):
            text = self.pdf_text_extractor.extract(file_path)

        # ❌ Otherwise → OCR
        else:
            text = self._ocr_file(file_path)

        output_path = OCR_DATA_DIR / f"{file_path.stem}.txt"
        output_path.write_text(text, encoding="utf-8")
        return output_path

    def _ocr_file(self, file_path: Path) -> str:
        texts = []

        if file_path.suffix.lower() == ".pdf":
            pages = convert_from_path(file_path, dpi=300)
            for page in pages:
                texts.append(self._ocr_image(page))
        else:
            image = Image.open(file_path)
            texts.append(self._ocr_image(image))

        return "\n\n".join(texts)

    def _ocr_image(self, image: Image.Image) -> str:
        processed = self.preprocessor.preprocess(image)
        encoded = self._encode_image(processed)

        response = client.chat.completions.create(
            model=OCR_MODEL,
            max_tokens=4092,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded}"
                            },
                        }
                    ],
                }
            ],
        )

        return response.choices[0].message.content.strip()

    @staticmethod
    def _encode_image(image: Image.Image) -> str:
        import base64
        from io import BytesIO

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
