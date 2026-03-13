from pydantic import BaseModel, Field


class GroundedAnswerRequest(BaseModel):
    question: str = Field(..., min_length=1)
    document_id: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    max_citations: int = Field(default=2, ge=1, le=5)


class Citation(BaseModel):
    citation_id: str
    chunk_id: str
    page_number: int
    chunk_index: int
    score: float
    excerpt: str


class GroundedAnswerResponse(BaseModel):
    question: str
    document_id: str
    answer_text: str
    answer_strategy: str
    top_k: int
    citations: list[Citation]
    latency_ms: int
