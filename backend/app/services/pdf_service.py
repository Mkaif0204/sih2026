import io
import logging
from typing import BinaryIO
import pypdf

logger = logging.getLogger(__name__)

FALLBACK_SYLLABUS = "Computer Science Core Engineering Curriculum"

class PDFService:
    """Service to safely extract syllabus and curriculum text from PDF files."""

    @staticmethod
    def extract_text(file_stream: BinaryIO) -> str:
        """
        Extract text from a binary PDF file stream.
        Falls back to default curriculum text if extraction fails or text is empty.
        """
        extracted_text = ""
        try:
            reader = pypdf.PdfReader(file_stream)
            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        except Exception as exc:
            logger.warning(f"Failed to extract text from PDF stream: {exc}")
            return FALLBACK_SYLLABUS

        cleaned_text = extracted_text.strip()
        if not cleaned_text:
            logger.warning("Extracted text from PDF was empty; using fallback.")
            return FALLBACK_SYLLABUS

        return cleaned_text

pdf_service = PDFService()
