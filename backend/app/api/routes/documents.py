from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_upload_dir
from app.repositories.documents import get_document, list_document_summaries, save_document
from app.schemas.documents import DocumentDetail, DocumentSummary, UploadResponse
from app.services.pdf_parser import PDFParseError, parse_pdf

router = APIRouter()


def _validate_pdf_filename(filename: str | None) -> str:
    safe_filename = Path(filename or "uploaded.pdf").name
    if not safe_filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF uploads are supported in the current MVP.",
        )
    return safe_filename


async def _save_upload(file: UploadFile, filename: str) -> Path:
    upload_dir = get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    stored_path = upload_dir / f"{uuid4().hex}{Path(filename).suffix.lower()}"
    stored_path.write_bytes(file_bytes)
    return stored_path


@router.get("", response_model=list[DocumentSummary])
def list_documents() -> list[DocumentSummary]:
    return list_document_summaries()


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document_detail(document_id: str) -> DocumentDetail:
    document = get_document(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' was not found.",
        )
    return document


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    filename = _validate_pdf_filename(file.filename)
    stored_path = await _save_upload(file, filename)

    try:
        pages = parse_pdf(stored_path)
    except PDFParseError as exc:
        stored_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    document = DocumentDetail(
        id=uuid4().hex,
        filename=filename,
        status="parsed",
        created_at=datetime.now(UTC),
        page_count=len(pages),
        extracted_char_count=sum(page.char_count for page in pages),
        pages=pages,
    )
    save_document(document)

    return UploadResponse(
        document=document,
        message="File uploaded and parsed successfully.",
    )
