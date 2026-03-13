import re

from app.schemas.documents import DocumentDetail
from app.schemas.retrieval import StoredChunk
from app.services.embeddings import embed_text

WORD_PATTERN = re.compile(r"\S+")
WORDS_PER_CHUNK = 90
OVERLAP_WORDS = 20


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _build_text_chunks(text: str) -> list[str]:
    words = WORD_PATTERN.findall(text)
    if not words:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = min(start + WORDS_PER_CHUNK, len(words))
        chunks.append(" ".join(words[start:end]).strip())
        if end >= len(words):
            break
        start = max(end - OVERLAP_WORDS, start + 1)

    return chunks


def build_document_chunks(document: DocumentDetail) -> list[StoredChunk]:
    chunks: list[StoredChunk] = []

    for page in document.pages:
        normalized_text = _normalize_text(page.text)
        page_chunks = _build_text_chunks(normalized_text)

        for chunk_index, chunk_text in enumerate(page_chunks):
            chunk_id = f"{document.document_id}_p{page.page_number}_c{chunk_index}"
            chunks.append(
                StoredChunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    char_count=len(chunk_text),
                    word_count=len(WORD_PATTERN.findall(chunk_text)),
                    text=chunk_text,
                    text_preview=chunk_text[:180],
                    embedding=embed_text(chunk_text),
                )
            )

    return chunks
