from datetime import UTC, datetime

from fastapi import APIRouter, File, UploadFile

from app.schemas.documents import DocumentSummary, UploadResponse

router = APIRouter()

_documents: list[DocumentSummary] = []


@router.get("", response_model=list[DocumentSummary])
def list_documents() -> list[DocumentSummary]:
    return _documents


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    document = DocumentSummary(
        id=str(len(_documents) + 1),
        filename=file.filename or "unknown",
        status="uploaded",
        created_at=datetime.now(UTC),
    )
    _documents.append(document)

    # This is a placeholder response. Actual file persistence and parsing
    # will be added in the next implementation step.
    return UploadResponse(document=document, message="File received. Parsing pipeline not connected yet.")
