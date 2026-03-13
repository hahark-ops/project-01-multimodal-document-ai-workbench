from fastapi import APIRouter

from app.api.routes import answers, documents, evaluations, health, retrieval, summaries

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
api_router.include_router(answers.router, prefix="/answers", tags=["answers"])
api_router.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
