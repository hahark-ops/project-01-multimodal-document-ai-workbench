from app.schemas.documents import DocumentDetail
from app.schemas.retrieval import (
    ChunkPreview,
    DocumentChunksResponse,
    RetrievalResult,
    RetrievalSearchResponse,
    StoredChunk,
)
from app.services.chunking import build_document_chunks
from app.services.embeddings import embed_text
from app.services.storage import load_all_document_chunks, load_document_chunks, save_document_chunks


class DocumentChunksNotFoundError(Exception):
    pass


def _dot_similarity(left: list[float], right: list[float]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))


def index_document_chunks(document: DocumentDetail) -> list[StoredChunk]:
    chunks = build_document_chunks(document)
    save_document_chunks(document.document_id, chunks)
    return chunks


def get_document_chunk_list(document_id: str) -> DocumentChunksResponse:
    chunks = load_document_chunks(document_id)
    if chunks is None:
        raise DocumentChunksNotFoundError(f"Chunks for document '{document_id}' were not found.")

    return DocumentChunksResponse(
        document_id=document_id,
        chunk_count=len(chunks),
        chunks=[
            ChunkPreview(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                char_count=chunk.char_count,
                word_count=chunk.word_count,
                text_preview=chunk.text_preview,
            )
            for chunk in chunks
        ],
    )


def search_document_chunks(
    query: str, *, document_id: str | None = None, top_k: int = 3
) -> RetrievalSearchResponse:
    normalized_query = query.strip()
    if not normalized_query:
        return RetrievalSearchResponse(query=query, document_id=document_id, top_k=top_k, results=[])

    if document_id:
        search_space = load_document_chunks(document_id)
        if search_space is None:
            raise DocumentChunksNotFoundError(f"Chunks for document '{document_id}' were not found.")
    else:
        search_space = load_all_document_chunks()

    query_embedding = embed_text(normalized_query)
    scored_chunks = [
        (_dot_similarity(query_embedding, chunk.embedding), chunk) for chunk in search_space
    ]
    ranked_chunks = sorted(
        scored_chunks,
        key=lambda item: (-item[0], item[1].page_number, item[1].chunk_index),
    )

    results = [
        RetrievalResult(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            page_number=chunk.page_number,
            chunk_index=chunk.chunk_index,
            char_count=chunk.char_count,
            word_count=chunk.word_count,
            score=round(score, 4),
            text=chunk.text,
        )
        for score, chunk in ranked_chunks[:top_k]
    ]

    return RetrievalSearchResponse(
        query=normalized_query,
        document_id=document_id,
        top_k=top_k,
        results=results,
    )
