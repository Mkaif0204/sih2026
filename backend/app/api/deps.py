from app.services.gemini_service import GeminiService, gemini_service
from app.services.pdf_service import PDFService, pdf_service
from app.services.telemetry_service import TelemetryService, telemetry_service

def get_gemini_service() -> GeminiService:
    return gemini_service

def get_pdf_service() -> PDFService:
    return pdf_service

def get_telemetry_service() -> TelemetryService:
    return telemetry_service
