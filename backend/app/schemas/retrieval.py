from pydantic import BaseModel, Field


class StoredChunk(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    char_count: int
    word_count: int
    text: str
    text_preview: str
    embedding: list[float]


class ChunkPreview(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    char_count: int
    word_count: int
    text_preview: str


class DocumentChunksResponse(BaseModel):
    document_id: str
    chunk_count: int
    chunks: list[ChunkPreview]


class RetrievalSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    document_id: str | None = None
    top_k: int = Field(default=3, ge=1, le=10)


class RetrievalResult(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    char_count: int
    word_count: int
    score: float
    text: str


class RetrievalSearchResponse(BaseModel):
    query: str
    document_id: str | None = None
    top_k: int
    results: list[RetrievalResult]
