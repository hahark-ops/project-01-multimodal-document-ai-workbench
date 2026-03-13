from fastapi import APIRouter, status

from app.errors import APIException
from app.schemas.documents import APIErrorResponse
from app.schemas.retrieval import RetrievalSearchRequest, RetrievalSearchResponse
from app.services.retrieval import DocumentChunksNotFoundError, search_document_chunks
from app.services.storage import ParsedDocumentLoadError

router = APIRouter()


@router.post(
    "/search",
    response_model=RetrievalSearchResponse,
    responses={400: {"model": APIErrorResponse}, 404: {"model": APIErrorResponse}},
)
def search_chunks(request: RetrievalSearchRequest) -> RetrievalSearchResponse:
    if not request.query.strip():
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_QUERY",
            message="Search query must include at least one non-space character.",
        )

    try:
        return search_document_chunks(
            request.query,
            document_id=request.document_id,
            top_k=request.top_k,
        )
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
