from fastapi import APIRouter, status

from app.errors import APIException
from app.schemas.answers import GroundedAnswerRequest, GroundedAnswerResponse
from app.schemas.documents import APIErrorResponse
from app.services.grounded_answer import answer_question
from app.services.retrieval import DocumentChunksNotFoundError
from app.services.storage import ParsedDocumentLoadError

router = APIRouter()


@router.post(
    "/ask",
    response_model=GroundedAnswerResponse,
    responses={400: {"model": APIErrorResponse}, 404: {"model": APIErrorResponse}},
)
def ask_grounded_question(request: GroundedAnswerRequest) -> GroundedAnswerResponse:
    if not request.question.strip():
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_QUESTION",
            message="Question must include at least one non-space character.",
        )

    try:
        return answer_question(
            request.question,
            document_id=request.document_id,
            top_k=request.top_k,
            max_citations=request.max_citations,
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
