# ingestion/image_preprocessor.py

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:
    """
    High-quality OCR preprocessing optimized for English documents.
    """

    def preprocess(self, image: Image.Image) -> Image.Image:
        """
        Apply a full preprocessing pipeline to improve OCR accuracy.
        """
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Increase contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(gray)

        # Denoise while preserving edges
        denoised = cv2.bilateralFilter(contrast, d=9, sigmaColor=75, sigmaSpace=75)

        # Adaptive thresholding (better for scanned docs)
        thresh = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10,
        )

        # Deskew
        deskewed = self._deskew(thresh)

        # Resize for better OCR (simulate ~300 DPI)
        resized = cv2.resize(
            deskewed,
            None,
            fx=1.5,
            fy=1.5,
            interpolation=cv2.INTER_CUBIC,
        )

        return Image.fromarray(resized)

    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Deskew image using minimum area rectangle.
        """
        coords = np.column_stack(np.where(image > 0))
        if coords.size == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        return cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )
