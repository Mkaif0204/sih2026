from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from app.api.deps import get_gemini_service, get_pdf_service
from app.models.gap_analysis import GapAnalysisRequest, GapAnalysisResponse
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PDFService

router = APIRouter()

@router.post(
    "/audit-file",
    response_model=GapAnalysisResponse,
    summary="Mode 1: Audit Syllabus PDF",
    description="Upload a university syllabus PDF and audit its alignment against target industry role criteria."
)
async def audit_syllabus_file(
    file: UploadFile = File(..., description="Syllabus PDF file"),
    target_role: str = Form("Software Engineer", description="Target industry job title"),
    pdf_service: PDFService = Depends(get_pdf_service),
    gemini_service: GeminiService = Depends(get_gemini_service),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a PDF."
        )

    try:
        syllabus_text = pdf_service.extract_text(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process PDF: {str(e)}"
        )

    return gemini_service.audit_curriculum(syllabus_text=syllabus_text, target_role=target_role)


@router.post(
    "/audit-text",
    response_model=GapAnalysisResponse,
    summary="Mode 1: Audit Syllabus Text",
    description="Provide raw curriculum or syllabus text to audit against target industry role criteria."
)
async def audit_syllabus_text(
    payload: GapAnalysisRequest,
    gemini_service: GeminiService = Depends(get_gemini_service),
):
    return gemini_service.audit_curriculum(
        syllabus_text=payload.syllabus_text,
        target_role=payload.target_role
    )
