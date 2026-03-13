from fastapi import APIRouter

from app.api.routes import documents, health, retrieval

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
