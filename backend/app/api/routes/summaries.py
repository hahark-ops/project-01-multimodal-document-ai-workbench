from fastapi import APIRouter, status

from app.errors import APIException
from app.schemas.documents import APIErrorResponse
from app.schemas.summaries import SummaryRequest, SummaryResponse
from app.services.retrieval import DocumentChunksNotFoundError
from app.services.storage import ParsedDocumentLoadError
from app.services.summary import generate_summary

router = APIRouter()


@router.post(
    "/generate",
    response_model=SummaryResponse,
    responses={404: {"model": APIErrorResponse}},
)
def generate_document_summary(request: SummaryRequest) -> SummaryResponse:
    try:
        return generate_summary(
            request.document_id,
            max_points=request.max_points,
            max_highlights=request.max_highlights,
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
