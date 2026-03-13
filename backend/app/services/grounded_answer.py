import re
import time

from app.schemas.answers import Citation, GroundedAnswerResponse
from app.services.retrieval import search_document_chunks

SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+|\n+")
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9']+")


def _tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text)}


def _split_sentences(text: str) -> list[str]:
    raw_sentences = [part.strip() for part in SENTENCE_SPLIT_PATTERN.split(text)]
    return [sentence for sentence in raw_sentences if sentence]


def _score_sentence(sentence: str, query_tokens: set[str], retrieval_score: float) -> float:
    sentence_tokens = _tokenize(sentence)
    lexical_overlap = len(query_tokens & sentence_tokens)
    return (lexical_overlap * 2.0) + retrieval_score


def answer_question(
    question: str,
    *,
    document_id: str,
    top_k: int = 3,
    max_citations: int = 2,
) -> GroundedAnswerResponse:
    started_at = time.perf_counter()
    retrieval_payload = search_document_chunks(
        question,
        document_id=document_id,
        top_k=top_k,
    )
    query_tokens = _tokenize(question)
    candidates: list[tuple[float, str, Citation]] = []

    for result in retrieval_payload.results:
        sentences = _split_sentences(result.text) or [result.text.strip()]
        for sentence in sentences:
            excerpt = sentence[:220].strip()
            citation = Citation(
                citation_id=f"cite_{result.chunk_id}",
                chunk_id=result.chunk_id,
                page_number=result.page_number,
                chunk_index=result.chunk_index,
                score=result.score,
                excerpt=excerpt,
            )
            candidates.append(
                (_score_sentence(sentence, query_tokens, result.score), sentence, citation)
            )

    candidates.sort(key=lambda item: item[0], reverse=True)

    selected_sentences: list[str] = []
    citations: list[Citation] = []
    used_chunk_ids: set[str] = set()

    for sentence_score, sentence, citation in candidates:
        if citation.chunk_id in used_chunk_ids:
            continue
        if len(citations) >= max_citations:
            break
        if sentence_score <= 0 and citations:
            break

        used_chunk_ids.add(citation.chunk_id)
        citations.append(citation)
        selected_sentences.append(sentence)

    if not citations and retrieval_payload.results:
        fallback = retrieval_payload.results[0]
        citations.append(
            Citation(
                citation_id=f"cite_{fallback.chunk_id}",
                chunk_id=fallback.chunk_id,
                page_number=fallback.page_number,
                chunk_index=fallback.chunk_index,
                score=fallback.score,
                excerpt=fallback.text[:220].strip(),
            )
        )

    if candidates and candidates[0][0] > 0 and selected_sentences:
        answer_text = "문서 근거 기준 답변: " + " ".join(selected_sentences)
    elif citations:
        answer_text = (
            "질문과 직접 일치하는 문장을 확정하진 못했지만, 가장 가까운 근거는 다음과 같습니다: "
            f"{citations[0].excerpt}"
        )
    else:
        answer_text = "문서에서 질문과 연결되는 근거를 찾지 못했습니다."

    latency_ms = int((time.perf_counter() - started_at) * 1000)

    return GroundedAnswerResponse(
        question=question.strip(),
        document_id=document_id,
        answer_text=answer_text,
        answer_strategy="extractive-grounded-baseline",
        top_k=top_k,
        citations=citations,
        latency_ms=latency_ms,
    )
