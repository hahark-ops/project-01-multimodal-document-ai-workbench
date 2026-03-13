from pathlib import Path

from fastapi import APIRouter, File, UploadFile, status

from app.errors import APIException
from app.schemas.documents import APIErrorResponse, DocumentDetail, PageSummary, UploadResponse
from app.schemas.retrieval import DocumentChunksResponse
from app.services.pdf_parser import PDFParseError, parse_pdf
from app.services.retrieval import DocumentChunksNotFoundError, get_document_chunk_list, index_document_chunks
from app.services.storage import (
    create_document_id,
    delete_document_assets,
    load_parsed_document,
    ParsedDocumentLoadError,
    save_parsed_document,
    save_upload_stream,
    StorageWriteError,
)

router = APIRouter()


def _validate_pdf_filename(filename: str | None) -> str:
    safe_filename = Path(filename or "uploaded.pdf").name
    if not safe_filename.lower().endswith(".pdf"):
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="UNSUPPORTED_FILE_TYPE",
            message="Only PDF files are supported in Phase 1.",
        )
    return safe_filename


def _build_upload_response(document: DocumentDetail) -> UploadResponse:
    return UploadResponse(
        document_id=document.document_id,
        filename=document.filename,
        status=document.status,
        page_count=document.page_count,
        chunk_count=document.chunk_count,
        pages=[
            PageSummary(
                page_number=page.page_number,
                char_count=page.char_count,
                text_preview=page.text[:180],
            )
            for page in document.pages
        ],
    )


@router.post(
    "/upload",
    response_model=UploadResponse,
    responses={400: {"model": APIErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    filename = _validate_pdf_filename(file.filename)
    document_id = create_document_id()
    try:
        stored_file, total_bytes = await save_upload_stream(document_id, file)
    except StorageWriteError as exc:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="FILE_SAVE_FAILED",
            message=str(exc),
        ) from exc

    if total_bytes == 0:
        stored_file.unlink(missing_ok=True)
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="EMPTY_FILE",
            message="Uploaded file is empty.",
        )

    try:
        pages = parse_pdf(stored_file)
    except PDFParseError as exc:
        stored_file.unlink(missing_ok=True)
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="PDF_PARSE_FAILED",
            message=str(exc),
        ) from exc

    parsed_document = DocumentDetail(
        document_id=document_id,
        filename=filename,
        status="parsed",
        page_count=len(pages),
        chunk_count=0,
        pages=pages,
    )
    try:
        chunks = index_document_chunks(parsed_document)
        parsed_document.chunk_count = len(chunks)
        save_parsed_document(parsed_document)
    except Exception as exc:
        delete_document_assets(document_id)
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="PARSED_DOCUMENT_SAVE_FAILED",
            message="Parsed document could not be indexed or saved.",
        ) from exc
    return _build_upload_response(parsed_document)


@router.get(
    "/{document_id}/chunks",
    response_model=DocumentChunksResponse,
    responses={404: {"model": APIErrorResponse}},
)
def get_document_chunks(document_id: str) -> DocumentChunksResponse:
    try:
        return get_document_chunk_list(document_id)
    except DocumentChunksNotFoundError as exc:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            code="DOCUMENT_CHUNKS_NOT_FOUND",
            message=str(exc),
        ) from exc
    except ParsedDocumentLoadError as exc:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DOCUMENT_CHUNKS_LOAD_FAILED",
            message=str(exc),
        ) from exc


@router.get(
    "/{document_id}",
    response_model=DocumentDetail,
    responses={404: {"model": APIErrorResponse}},
)
def get_document(document_id: str) -> DocumentDetail:
    try:
        document = load_parsed_document(document_id)
    except ParsedDocumentLoadError as exc:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="PARSED_DOCUMENT_LOAD_FAILED",
            message=str(exc),
        ) from exc
    if document is None:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            code="DOCUMENT_NOT_FOUND",
            message=f"Document '{document_id}' was not found.",
        )
    return document
