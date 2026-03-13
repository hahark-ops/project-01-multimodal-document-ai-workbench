from fastapi import APIRouter, status

from app.errors import APIException
from app.schemas.documents import APIErrorResponse
from app.schemas.evaluations import EvaluationRunRequest, EvaluationRunResponse
from app.services.evaluation import EvaluationSuiteNotFoundError, run_evaluation
from app.services.retrieval import DocumentChunksNotFoundError
from app.services.storage import ParsedDocumentLoadError

router = APIRouter()


@router.post(
    "/run",
    response_model=EvaluationRunResponse,
    responses={404: {"model": APIErrorResponse}},
)
def run_document_evaluation(request: EvaluationRunRequest) -> EvaluationRunResponse:
    try:
        return run_evaluation(
            request.document_id,
            suite_id=request.suite_id,
            top_k=request.top_k,
            max_citations=request.max_citations,
        )
    except EvaluationSuiteNotFoundError as exc:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            code="EVALUATION_SUITE_NOT_FOUND",
            message=str(exc),
        ) from exc
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
