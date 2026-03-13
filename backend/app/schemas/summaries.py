from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    max_points: int = Field(default=3, ge=1, le=5)
    max_highlights: int = Field(default=3, ge=1, le=5)


class SummaryHighlight(BaseModel):
    highlight_id: str
    page_number: int
    chunk_index: int
    importance_score: float
    excerpt: str


class SummaryResponse(BaseModel):
    document_id: str
    summary_text: str
    key_points: list[str]
    highlights: list[SummaryHighlight]
    summary_strategy: str
    latency_ms: int
