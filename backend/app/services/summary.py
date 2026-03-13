import re
import time

from app.schemas.summaries import SummaryHighlight, SummaryResponse
from app.services.storage import load_document_chunks

CLAUSE_HINTS = (
    "contractual status",
    "time of performance",
    "compensation",
    "invoice",
    "taxes",
    "situs",
    "assignment",
)
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+|\n+")


def _split_sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in SENTENCE_SPLIT_PATTERN.split(text) if sentence.strip()]


def _score_sentence(sentence: str, page_number: int) -> float:
    lowered = sentence.lower()
    score = 0.0

    if sentence.startswith("("):
        score += 3.0
    if any(hint in lowered for hint in CLAUSE_HINTS):
        score += 4.0
    if 40 <= len(sentence) <= 240:
        score += 2.0

    score += max(0.0, 2.0 - (page_number - 1) * 0.25)
    return score


def generate_summary(
    document_id: str,
    *,
    max_points: int = 3,
    max_highlights: int = 3,
) -> SummaryResponse:
    started_at = time.perf_counter()
    chunks = load_document_chunks(document_id)
    if chunks is None:
        from app.services.retrieval import DocumentChunksNotFoundError

        raise DocumentChunksNotFoundError(f"Chunks for document '{document_id}' were not found.")

    candidates: list[tuple[float, str, SummaryHighlight]] = []

    for chunk in chunks:
        for sentence in _split_sentences(chunk.text) or [chunk.text.strip()]:
            excerpt = sentence[:220].strip()
            highlight = SummaryHighlight(
                highlight_id=f"summary_{chunk.chunk_id}",
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                importance_score=0.0,
                excerpt=excerpt,
            )
            score = _score_sentence(sentence, chunk.page_number)
            highlight.importance_score = round(score, 4)
            candidates.append((score, sentence, highlight))

    candidates.sort(key=lambda item: item[0], reverse=True)

    selected_sentences: list[str] = []
    highlights: list[SummaryHighlight] = []
    used_excerpts: set[str] = set()

    for score, sentence, highlight in candidates:
        if highlight.excerpt in used_excerpts:
            continue
        used_excerpts.add(highlight.excerpt)

        if len(selected_sentences) < max_points:
            selected_sentences.append(sentence)
        if len(highlights) < max_highlights:
            highlights.append(highlight)
        if len(selected_sentences) >= max_points and len(highlights) >= max_highlights:
            break

    summary_text = "문서 요약: " + " ".join(selected_sentences) if selected_sentences else "요약할 문장을 찾지 못했습니다."
    key_points = [highlight.excerpt for highlight in highlights[:max_points]]
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    return SummaryResponse(
        document_id=document_id,
        summary_text=summary_text,
        key_points=key_points,
        highlights=highlights,
        summary_strategy="extractive-summary-baseline",
        latency_ms=latency_ms,
    )
