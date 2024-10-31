import os
from typing import Optional
import PyPDF2


class PDFValidator:
    @staticmethod
    def validate_pdf_path(pdf_path: str) -> tuple[bool, Optional[str]]:
        """Validate if the given path points to a valid PDF file.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not pdf_path:
            return False, "PDF path cannot be empty"

        if not os.path.exists(pdf_path):
            return False, f"File not found: {pdf_path}"

        if not pdf_path.lower().endswith('.pdf'):
            return False, "File must be a PDF"

        try:
            with open(pdf_path, 'rb') as f:
                PyPDF2.PdfReader(f)
            return True, None
        except Exception as e:
            return False, f"Invalid PDF file: {str(e)}"

    @staticmethod
    def validate_content(text: str) -> tuple[bool, Optional[str]]:
        """Validate if the extracted text content is valid for processing.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Extracted text is empty"

        # Add minimum length check
        if len(text.split()) < 50:  # Arbitrary minimum word count
            return False, "Text content too short for meaningful flashcard generation"

        return True, None
